import requests
import json
import os
import re
from packaging import version

requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

def main():
    # 读取当前版本
    maker_file = os.path.join(os.getcwd(), 'maker.json')
    current_version = "0.0.0"  # 默认版本
    
    try:
        if os.path.exists(maker_file):
            with open(maker_file, 'r', encoding='utf-8') as file:
                data_json = json.load(file)
            current_version = data_json.get('version', '0.0.0')
    except Exception as e:
        print(f"读取版本信息失败: {str(e)}")
    
    # 获取最新版本信息
    url = "https://api.github.com/repos/shuaiqiyy/homework-killer/releases"
    
    try:
        # 设置请求超时和重试
        response = requests.get(url, timeout=(5, 10), verify=False)
        response.raise_for_status()
        
        releases = response.json()
        
        # 验证API返回结构
        if not isinstance(releases, list) or len(releases) == 0:
            return "GitHub返回了无效的响应格式"
        
        # 获取最新正式版（跳过预发布版本）
        latest_release = None
        for release in releases:
            if not release.get('prerelease', True):
                latest_release = release
                break
        
        if not latest_release:
            return "未找到正式发布版本"
        
        latest_version = latest_release['tag_name']
        
        # 标准化版本号比较
        try:
            current_ver = version.parse(current_version)
            latest_ver = version.parse(latest_version)
        except Exception:
            # 版本号格式异常时使用字符串比较
            if latest_version == current_version:
                return f"当前版本 {current_version} 已是最新版本"
            else:
                pass  # 继续执行更新提示
        else:
            if latest_ver <= current_ver:
                return f"当前版本 {current_version} 已是最新版本"
        
        # 获取实际下载页面（非API链接）
        html_url = latest_release['html_url']
        
        return (
            f"发现新版本 {latest_version}\n"
            f"当前版本: {current_version}\n\n"
            f"请访问以下链接查看更新内容并下载:\n"
            f"{html_url}\n\n"
            f"更新说明:\n{latest_release.get('body', '暂无说明')}"
        )
    
    except requests.exceptions.Timeout:
        return "连接GitHub超时，请检查网络连接"
    except requests.exceptions.HTTPError as e:
        return f"HTTP错误: {e.response.status_code} - {e.response.reason}"
    except requests.exceptions.RequestException as e:
        return f"网络请求失败: {str(e)}"
    except json.JSONDecodeError:
        return "解析GitHub响应失败"
    except KeyError as e:
        return f"API响应缺少关键字段: {str(e)}"
    except Exception as e:
        return f"检查更新失败: {str(e)}"