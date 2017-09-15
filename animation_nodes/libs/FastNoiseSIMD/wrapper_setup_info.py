import os
import subprocess

directory = os.path.dirname(__file__)
sourceDir = os.path.join(directory, "source")

def getCompileLibraryTasks(utils):
    return [compile_FastNoiseSIMD]

def compile_FastNoiseSIMD(utils):
    print("Compile FastNoiseSIMD\n")

    sourceFiles = list(utils.iterPathsWithExtension(sourceDir, [".cpp", ".h"]))
    targetName, command, _ = getCompileInfo(utils)
    targetFile = os.path.join(sourceDir, targetName)

    if utils.dependenciesChanged(targetFile, sourceFiles):
        subprocess.run(command)
    else:
        print("Nothing changed. Skipping.")

def getExtensionArgs(utils):
    args = getCompileInfo(utils)[2]
    args["library_dirs"] = [sourceDir]
    return args

def getCompileInfo(utils):
    if utils.onWindows:
        return ("FastNoiseSIMD_windows.lib",
                [os.path.join(sourceDir, "compile_windows.bat")],
                {"libraries" : ["FastNoiseSIMD_windows"],
                 "extra_link_args" : ["/NODEFAULTLIB:LIBCMT"]})
    if utils.onLinux:
        return ("libFastNoiseSIMD_linux.a",
                ["sh", os.path.join(sourceDir, "compile_linux.sh")],
                {"libraries" : ["FastNoiseSIMD_linux"],
                 "extra_compile_args" : ["-std=c++11"]})
    if utils.onMacOS:
        return ("libFastNoiseSIMD_macos.a",
                ["sh", os.path.join(sourceDir, "compile_macos.sh")],
                {"libraries" : ["FastNoiseSIMD_macos"],
                 "extra_compile_args" : ["-std=c++11"]})
    raise Exception("unknown platform")
