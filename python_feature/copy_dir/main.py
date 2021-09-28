import os
import glob


src = ".\\config37"
dst = ".\\config37-fangzhen"


def CopyFileOrDir(srcDir, dstDir):
    baseName = os.path.basename(srcDir)
    targetFileOrDirName = os.path.join(dstDir, baseName)
    if baseName == "Actor":
        paths = targetFileOrDirName.split("\\")
        targetFileOrDirName = "\\".join(paths[:-1])
    print(baseName, targetFileOrDirName)
    if os.path.isfile(srcDir):
        open(targetFileOrDirName, "wb").write(open(srcDir, "rb").read())
    else:
        try:
            os.makedirs(targetFileOrDirName)
        except Exception as error:
            print(error)
        srcFilesDirs = os.listdir(srcDir)
        for fileOrDir in srcFilesDirs:
            srcFileOrDirPath = os.path.join(srcDir, fileOrDir)
            CopyFileOrDir(srcFileOrDirPath, targetFileOrDirName)


# def change_process():

if __name__ == "__main__":
    CopyFileOrDir(".\\Actor", ".\\Actor_copy")
    # os.makedirs(".\\Actor_copy")

