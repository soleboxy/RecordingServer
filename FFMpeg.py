import os
import subprocess


class FFMpeg(object):

    def __init__(self, source, destination, timeout=10, *args, **kwargs):
        super(FFMpeg, self).__init__(*args, **kwargs)
        self.ffmpeg = "/usr/bin/ffmpeg"
        self.source = source
        self.destination = destination + ".avi"
        self.timeout = timeout
        codec = "libx264"
        preset = "medium"
        resolution = "1920x1200"
        vide_buffer = "400k"
        format = "avi"
        audio_codec = ["aac", "-strict", "-2", "-ab", "48k", "-ac", "2", "-ar", "44100"]
        self.ffmpeg_command = [self.ffmpeg, "-i", self.source, "-vcodec", codec, "-preset:v", preset, "-s",
                               resolution, "-b:v", vide_buffer, "-acodec"] + audio_codec +\
                              ['-f', format, self.destination]

        self.complete_object_for_ffmpeg_run = None


    @property
    def pid(self):
        return self.complete_object_for_ffmpeg_run.pid

    def record(self, **kwargs):
        """
        start recording stream , if timeout == 0 record forever
        :param source: url/path
        :param destination: path
        :param timout: the amount of time to record
        :return: pid of the ffmpeg recording proc in session
        """
        source = kwargs.get("source", self.source)
        destination = kwargs.get("destination", self.destination)
        timeout = kwargs.get("timeout", self.timeout)
        print("executing {}".format(self.ffmpeg_command))
        self.complete_object_for_ffmpeg_run = subprocess.run(self.ffmpeg_command, shell=False, timeout=timeout)
        return self.complete_object_for_ffmpeg_run  # fixme, need to return pid or something

    def size(self):
        """
        get current destination file_size
        :return: the size of the file being currently generated by ffmpeg
        """
        size = os.stat(self.destination).st_size
        return size

    def stop_recording(self):
        """
        kills the recording process
        :return:
        """
        self.complete_object_for_ffmpeg_run.kill()

if __name__ == "__main__":
    ffmpeg = FFMpeg("http://10.62.2.153/hdmi", "/home/sole/recordings/moo.mp4", 20)
    ffmpeg.record()