# Leetcode-CN Exporter 力扣(中国)导出器

## Introduction 简介

This script can export your code record (Solved) to csv file or excel file.

本脚本可以帮助您导出您的已完成题目的记录到csv或excel文件中

## Settings 预先设置
(English)
1. Add your Username and Password to ```config/PASSWD.py```
2. Download the driver to the ```bin/driver``` directory and add the directory into ```PATH```, download link can be found [here](bin/driver/download.md)

(Chinese)
1. 将您的用户名和密码写入```config/PASSWD.py```用于自动登录
2. 下载不同浏览器的驱动到```bin/driver```文件夹中并将其加入环境变量```PATH```，下载链接可以在[这里](bin/driver/download.md)中找到

## Dependence 依赖

```shell
pip install pandas selenium openpyxl beautifulsoup4
```

## Future Work 未来计划

- [ ] GUI Support
- [ ] Post Record Download
- [ ] Plan Switch