# Creating Gem5 Disk Image

### Create Empty Disk Image

Create an Empty Disk Image of size 4GB (1M\*4096):
```
$ dd if=/dev/zero of=linux-x86.img oflag=direct bs=1M count=4096
4096+0 records in
4096+0 records out
4294967296 bytes (4.3 GB, 4.0 GiB) copied, 5.5287 s, 777 MB/s
```

### Attach Image as Loop Device

The next step is to attach the newly created disk image as a [loop device](https://en.wikipedia.org/wiki/Loop_device#:~:text=In%20Unix%2Dlike%20operating%20systems,existing%20file%20in%20the%20filesystem).

To mount the image as a loop device we use the *losetup* utility:
```
$ sudo losetup -f --partscan linux-x86.img
```

Check which loop device was assigned to the image with:
```
$ sudo losetup -l
NAME       SIZELIMIT OFFSET AUTOCLEAR RO BACK-FILE                    DIO LOG-SEC
...
/dev/loop5         0      0         0  0 /path/to/image/linux-x86.img   0     512
...
```

To unmount the loop device:
```
$ sudo losetup -d /dev/loop5
```

### Creating the Partition Table

With the image mounted as a loop device, the next step is to create the partition table. The utility used for this is *fdisk*.
```
$ sudo fdisk /dev/loop5
```

This will launch the fdisk utility and it will automatically create a new DOS disklabel. The next step is to create a new partiton:
```
Command (m for help): n
```

Select *p* for primary partition, and 1 for the partiion number. choose the defaults for the first and last sectors. Now if you enter p you should see an output similar to:
```
Command (m for help): p
Disk /dev/loop5: 4 GiB, 4294967296 bytes, 8388608 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xa408e4c2

Device       Boot Start     End Sectors Size Id Type
/dev/loop5p1       2048 8388607 8386560   4G 83 Linux
```

To write the changes and exit fdisk, enter the *w* command. To verify the changes have been written:
```
$ sudo fdisk -l linux-x86.img
Disk linux-x86.img: 4 GiB, 4294967296 bytes, 8388608 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xa408e4c2

Device         Boot Start     End Sectors Size Id Type
linux-x86.img1       2048 8388607 8386560   4G 83 Linux
```

### Creating the Filesystem

The next step is to create an ext4 filesystem on the first partition *p1* of the disk:
```
$ sudo mkfs -t ext4 /dev/loop5p1
mke2fs 1.45.5 (07-Jan-2020)
Discarding device blocks: done                            
Creating filesystem with 1048320 4k blocks and 262144 inodes
Filesystem UUID: 5f86ace8-f360-4b9b-b42b-8bfbec224889
Superblock backups stored on blocks: 
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done
```

### Mounting the Disk Image

At this point the disk image can be mounted to the file system:
```
$ mkdir mnt
$ sudo mount -o loop,offset=1048576 linux-x86.img mnt/
```

Verify that the image mounted and that the file system is set up correctly, there
should be a lost+found directory inside the image.
```
$ ls -l mnt
total 16
drwx------ 2 root root 16384 Jun  3 12:01 lost+found
```

### Adding the Base Files to the Image:

Next the root directory files must be added to the image. To install the root
directory files, first obtain a copy from
[ubuntu-base](http://cdimage.ubuntu.com/ubuntu-base/releases/). In this example
I am using kernel 5.4.44 and release 20.04. With the disk image mounted to
./mnt:
```
$ sudo tar -xvf ubuntu-base-20.04-base-amd64.tar.gz -C ./mnt
```

### Chroot & Update Software

Next, the disk image needs to be prepared, updated, and software installed so
that the benchmarks can be built and run. The image does not have a proper
`resolve.conf` file so it will not be able to get updates, however the hosts
`resolve.conf` file can be imported into the disk image.
```
$ sudo cp /etc/resolv.conf mnt/etc/resolv.conf
```

Before chroot, the `/sys /dev /proc` directories must be bound to the mount.
```
$ sudo mount -o bind /sys mnt/sys
$ sudo mount -o bind /dev mnt/dev
$ sudo mount -o bind /proc mnt/proc
```

Finally chroot into the mount
```
sudo chroot mnt /bin/bash
```

At this point we have changed the effective root of our system and we will now
be able to update, upgrade, and install software packages.
```
\# apt-get update && apt-get upgrade && apt-get install make gcc g++
```

### Exiting and Unmounting

To exit the chroot, simply type exit and you will return back. To safely
unmount everything, first unmout the mnt/sys mnt/dev mnt/proc that were bound
from the host.
```
$ sudo umount mnt/sys
$ sudo umount mnt/proc
$ sudo umount mnt/dev
```

Now the image can be unmounted from out mount point:
```
$ sudo umount mnt
```
