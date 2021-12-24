# 接口自动化测试框架

## 环境
* python 3.9.7
* 进入config目录，安装相关依赖包
  > pip install -r requirements

## 版本更新
### V2.0
####新增功能:
```
* 新增--save_result参数保存测试结果
  * 如果需要保存结果，就需要加actual_rc和actual_result到excel表里
* 每个API测试前会自动Login，token将保存到内存中 
* 新增用例控制yaml 
* 新增自动生成用例控制yaml, 自动保存到`interface/data/`目录下
  * 例子: python interface.py tool --data_file C:\test\newben_cli_arm64.xlsx --cases generate_suits
```

### 应用
```
python interface.py cli --data_file C:\test\newben_cli_arm64.xlsx  --ip 192.168.5.9 --sys_pwd testnb --not_email --suite_file C:\Project\Python\ghostcloudtest\interface\data\newben_cli_arm64_suites.
yaml
```
## 版本更新
### V2.1
####新增功能:
```
* 新增支持变量定义
  * interface\[api/cli]\config\config.yaml里面定义变量
  * 在excel表里$<变量名>引用
* 每个用例之间间隔时间设置
  * excel表里面增加interval_time参数，可以查看interface\data\api.xlsx例子
* 认证信息参数化
  通过--ip, --sys_user, --sys_pwd 赋值
    * python .\interface.py api --data_file .\interface\data\api.xlsx --suite_file .\interface\data\api.yaml --ip 192.168.5.61 --sys_user admin --sys_pwd password
* excel表里新增get_token sheet, 实现自动获取token
```