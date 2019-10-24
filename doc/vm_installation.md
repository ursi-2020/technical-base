[Sommaire](https://ursi-2020.github.io/Documentation/)

# VM installation:

- Download the latest version of [VirtualBox](https://www.virtualbox.org/).
- Download the [image](https://drive.google.com/open?id=1BLdizHalsrjGGgURnuTWLhyDRu_kr73Z) of the VM.
- Launch VirtualBox.
- Import a new VM.


![newVM](./images/newVM.png)
- Select the downloaded file.
![dlfile](./images/select_dl_file.png)
- Import without changing any options.
![import](./images/import.png)
- "Configuration > Shared Folder".
![config](./images/configuration.png)
![sharedFolder](./images/shared_folder.png)
### Change technical-base to the name of your GIT repository of your APP!
- Edit the shared folder so that it points to the previously cloned local git repository. Don't change the VM mounting point !!
![link](./images/link.png)
- Right click on the machine > start > start without display.
![start](./images/start.png)

## SSH VM connection:

Open a terminal in the Host machine and write the following command in:
```
ssh dev@localhost -p 22031
```
Default password is "dev".
The shared folder is located at the following path: 
```
/mnt/technical_base/
```
## Basic error

### Windows :

If you can not launch the vm with virtual Box and you got (check the error code you got on google):
```
Windows 10 Tech Preview
```
Follow this [tutorial](https://appuals.com/fix-hypervisor-is-not-running-error-on-windows-10/)

If you got this error :
```
Error 0x80070057
```

Follow this [tutorial](https://appuals.com/windows-update-error-0x80070057-fix/)
The method 2 works well.
