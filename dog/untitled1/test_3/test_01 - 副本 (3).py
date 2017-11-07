# 生成并运行bat
def updateIcons(project=projInfo):
    # 找到bat文件
    basetBat = '%s%s' % (baseFolder, 'aasIcons.bat')
    readInfos = checkFileRead(basetBat)
    # 处理信息
    projIconBat = []
    for info in readInfos:
        if '\\\\aas_repos\\\\aas_icons' in info:
            info = info.replace('\\\\aas_repos\\\\aas_icons', '%s\\\\%s' % ('\\\\aas_repos\\\\aas_icons', project))
        if '\\\\aas_tools\\\\aas_icons' in info:
            info = info.replace('\\\\aas_tools\\\\aas_icons', '%s\\\\%s' % ('\\\\aas_tools\\\\aas_icons', project))
        projIconBat.append(info)
    # 项目bat
    projBatFile = ('%s%s_%s.bat' % (baseFolder, 'aasIcons', project))
    checkFileWrite(projBatFile, projIconBat)
    # 运行
    subprocess.call(projBatFile, shell=True)