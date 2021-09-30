import platform


class VolumeControl:
    def __init__(self):
        self.os_type = platform.system()
        self.release = platform.release()
        print("You are running on {} Operating System and {} release ...".format(
            self.os_type, self.release))

        self.original_volume = 0

    def set_volume(self, target_volume):
        if self.os_type.lower() == "darwin":
            self._osx_volume_control(target_volume)
        else:
            print("Volume control not yet implemented")

    @staticmethod
    def _osx_volume_control(target_volume):
        import osascript
        vol = "set volume output volume " + str(target_volume)
        osascript.osascript(vol)

    @staticmethod
    def _win_volume_control():
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        # Volume related initializations
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        print(volume.GetVolumeRange())  # (-65.25, 0.0)

        pass

    @staticmethod
    def _linux_volume_control():
        pass
