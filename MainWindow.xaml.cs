using Microsoft.Win32;
using System;
using System.Diagnostics;
using System.Linq;
using System.Windows;

namespace MSPCManagerHelper
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            MainComboBox.SelectionChanged += MainComboBox_SelectionChanged;
            RefreshButton_Click(this, new RoutedEventArgs()); // 初始化时检测版本号
        }

        private void MainComboBox_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            if (FeatureComboBox == null)
                return;

            FeatureComboBox.Items.Clear();
            switch (MainComboBox.SelectedIndex)
            {
                case 1: // 主项目
                    FeatureComboBox.Items.Add("* 修复微软电脑管家无法安装 / 打开");
                    FeatureComboBox.Items.Add("* 获取微软电脑管家日志");
                    break;
                case 2: // 安装项目
                    FeatureComboBox.Items.Add("从 WinGet 下载微软电脑管家");
                    FeatureComboBox.Items.Add("从 Microsoft Store 下载微软电脑管家");
                    FeatureComboBox.Items.Add("为 所有用户 安装微软电脑管家");
                    FeatureComboBox.Items.Add("为 当前用户 安装微软电脑管家");
                    break;
                case 3: // 卸载项目
                    FeatureComboBox.Items.Add("为 所有用户 卸载微软管家");
                    FeatureComboBox.Items.Add("为 当前用户 卸载微软电脑管家");
                    FeatureComboBox.Items.Add("卸载微软电脑管家公测版");
                    break;
                case 4: // 其它项目
                    FeatureComboBox.Items.Add("查看当前电脑已安装的防病毒软件");
                    FeatureComboBox.Items.Add("开发者选项页");
                    FeatureComboBox.Items.Add("* 修复 Microsoft Edge (WebView2 Runtime) 无法安装");
                    FeatureComboBox.Items.Add("微软电脑管家常见问题解答");
                    FeatureComboBox.Items.Add("* 安装 Microsoft Edge WebView2 Runtime");
                    FeatureComboBox.Items.Add("加入微软电脑管家预览体验计划");
                    FeatureComboBox.Items.Add("重启微软电脑管家服务");
                    FeatureComboBox.Items.Add("* 切换微软电脑管家地区至中国");
                    break;
            }
        }

        private void FeatureExecuteButton_Click(object sender, RoutedEventArgs e)
        {
            if (MainComboBox.SelectedIndex == 0 || FeatureComboBox.SelectedIndex == -1)
            {
                MessageBox.Show("请选择要执行的功能");
                return;
            }

            CancelFeatureButton.IsEnabled = true;
            ResultTextBox.Text = $"正在执行 {FeatureComboBox.SelectedItem} 的操作...\n";

            // --------------------- 功能绑定区域 开始 ---------------------
            switch (FeatureComboBox.SelectedItem.ToString())
            {
                // "查看当前电脑已安装的防病毒软件" 功能区域 绑定
                case "查看当前电脑已安装的防病毒软件":
                    ExecutePowerShellScript();
                    break;

                // "开发者选项页" 功能区域 绑定
                case "开发者选项页":
                    OpenDeveloperSettingsPage();
                    break;

                // "修复 Microsoft Edge (WebView2 Runtime) 无法安装" 功能区域 绑定
                case "* 修复 Microsoft Edge (WebView2 Runtime) 无法安装":
                    FixWebView2Installation();
                    break;

                // "微软电脑管家常见问题解答" 功能区域
                case "微软电脑管家常见问题解答":
                    OpenDocURL();
                    break;

                // "加入微软电脑管家预览体验计划" 功能区域
                case "加入微软电脑管家预览体验计划":
                    OpenJoinInsiderURL();
                    break;

                // "重启微软电脑管家服务" 功能区域 绑定
                case "重启微软电脑管家服务":
                    RestartPCManagerService();
                    break;

                // "切换微软电脑管家地区至中国" 功能区域 绑定
                case "* 切换微软电脑管家地区至中国":
                    ChangeRegionToCN();
                    break;

                // 在这里添加其他功能的执行代码
                default:
                    ResultTextBox.Text += "操作完成。\n";
                    break;
            }
            // --------------------- 功能绑定区域 结束 ---------------------

            CancelFeatureButton.IsEnabled = false;
        }

        // --------------------- 功能区域 开始 ---------------------
        // "查看当前电脑已安装的防病毒软件" 功能区域 开始
        private void ExecutePowerShellScript()
        {
            try
            {
                var startInfo = new ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    Arguments = "-NoProfile -ExecutionPolicy Bypass -Command \"Get-WmiObject -Namespace 'Root\\SecurityCenter2' -Class 'AntivirusProduct' | Select-Object displayName, pathToSignedProductExe, pathToSignedReportingExe, productState | Format-List\"",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using (var process = Process.Start(startInfo))
                {
                    if (process == null)
                    {
                        ResultTextBox.Text += "无法启动 PowerShell 进程。\n";
                        return;
                    }

                    using (var reader = process.StandardOutput)
                    {
                        string result = reader.ReadToEnd();
                        FormatAndDisplayResult(result);
                    }
                }
            }
            catch (Exception ex)
            {
                ResultTextBox.Text += $"执行 PowerShell 脚本时出错: {ex.Message}\n";
            }
        }

        private void FormatAndDisplayResult(string? result)
        {
            if (string.IsNullOrEmpty(result))
            {
                ResultTextBox.Text += "未能获取到任何结果。\n";
                return;
            }

            var lines = result.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            string displayName = string.Empty;
            string pathToSignedProductExe = string.Empty;
            string pathToSignedReportingExe = string.Empty;
            string productState = string.Empty;

            foreach (var line in lines)
            {
                var parts = line.Split(new[] { ':' }, 2);
                if (parts.Length == 2)
                {
                    var key = parts[0].Trim();
                    var value = parts[1].Trim();

                    switch (key)
                    {
                        case "displayName":
                            displayName = value;
                            break;
                        case "pathToSignedProductExe":
                            pathToSignedProductExe = value;
                            break;
                        case "pathToSignedReportingExe":
                            pathToSignedReportingExe = value;
                            break;
                        case "productState":
                            productState = value;
                            break;
                    }
                }
            }

            ResultTextBox.Text += $"\n显示名称：{displayName}\n";
            ResultTextBox.Text += $"可执行文件路径：{pathToSignedProductExe}\n";
            ResultTextBox.Text += $"可执行文件路径：{pathToSignedReportingExe}\n";
            ResultTextBox.Text += $"状态：{productState}\n";
        }
        // "查看当前电脑已安装的防病毒软件" 功能区域 结束

        // "开发者选项页" 功能区域 开始
        private void OpenDeveloperSettingsPage()
        {
            try
            {
                Process.Start(new ProcessStartInfo("ms-settings:developers") { UseShellExecute = true });
                ResultTextBox.Text += "开发者选项页已打开。\n";
            }
            catch (Exception ex)
            {
                ResultTextBox.Text += $"打开开发者选项页时出错: {ex.Message}\n";
            }
        }
        // "开发者选项页" 功能区域 结束

        // "微软电脑管家常见问题解答" 功能区域 开始
        private void OpenDocURL()
        {
            try
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = "explorer.exe",
                    Arguments = "https://docs.qq.com/doc/DR2FrVkJmT0NuZ0Zx",
                    UseShellExecute = true
                });

                ResultTextBox.Text += "微软电脑管家常见问题解答已打开。\n";
            }
            catch (Exception ex)
            {
                ResultTextBox.Text += $"打开 URL 时出错: {ex.Message}\n";
            }
        }
        // "微软电脑管家常见问题解答" 功能区域 结束

        // "加入微软电脑管家预览体验计划" 功能区域 开始
        private void OpenJoinInsiderURL()
        {
            try
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = "explorer.exe",
                    Arguments = "https://forms.office.com/r/v1LX7SKWTs",
                    UseShellExecute = true
                });

                ResultTextBox.Text += "微软电脑管家预览体验计划表单已打开。\n";
            }
            catch (Exception ex)
            {
                ResultTextBox.Text += $"打开 URL 时出错: {ex.Message}\n";
            }
        }
        // "加入微软电脑管家预览体验计划" 功能区域 结束

        // "修复 Microsoft Edge (WebView2 Runtime) 无法安装" 功能区域 开始
        private void FixWebView2Installation()
        {
            try
            {
                const string registryPath = @"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options";
                const string keyName = "MicrosoftEdgeUpdate.exe";
                const string valueName = "DisableExceptionChainValidation";
                const int valueData = 0;

                // 删除注册表项
                using (RegistryKey? key = Registry.LocalMachine.OpenSubKey(registryPath, writable: true))
                {
                    if (key != null)
                    {
                        using (RegistryKey? subKey = key.OpenSubKey(keyName, writable: true))
                        {
                            if (subKey != null)
                            {
                                key.DeleteSubKey(keyName, throwOnMissingSubKey: false);
                                ResultTextBox.Text += "已删除注册表项。\n";
                            }
                        }
                    }
                }

                // 创建注册表项
                using (RegistryKey? key = Registry.LocalMachine.CreateSubKey($"{registryPath}\\{keyName}"))
                {
                    if (key != null)
                    {
                        key.SetValue(valueName, valueData, RegistryValueKind.DWord);
                        ResultTextBox.Text += "已重新创建注册表项并设置值。\n";
                    }
                }
            }
            catch (Exception ex)
            {
                ResultTextBox.Text += $"修复 Microsoft Edge 安装时出错: {ex.Message}\n";
            }
        }
        // "修复 Microsoft Edge (WebView2 Runtime) 无法安装" 功能区域 结束

        // "重启微软电脑管家服务" 功能区域 开始
        private void RestartPCManagerService()
        {
            try
            {
                // 停止服务
                ExecuteCommand("sc.exe", "stop \"PCManager Service Store\"");
                ResultTextBox.Text += "服务停止命令已执行。\n";

                // 等待一段时间以确保服务停止
                System.Threading.Thread.Sleep(3000); // 等待 3 秒

                // 启动服务
                ExecuteCommand("sc.exe", "start \"PCManager Service Store\"");
                ResultTextBox.Text += "服务启动命令已执行。\n";
            }
            catch (Exception ex)
            {
                ResultTextBox.Text += $"执行服务操作时出错: {ex.Message}\n";
            }
        }
        // "重启微软电脑管家服务" 功能区域 结束

        // 通用命令执行方法 开始
        private void ExecuteCommand(string fileName, string arguments)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = fileName,
                Arguments = arguments,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };

            using (var process = Process.Start(startInfo))
            {
                if (process == null)
                {
                    throw new InvalidOperationException("无法启动进程.");
                }

                // 读取输出和错误信息
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();

                process.WaitForExit();

                if (process.ExitCode != 0)
                {
                    throw new InvalidOperationException($"命令执行失败: {error}");
                }

                // 输出结果到 ResultTextBox
                ResultTextBox.Text += output + "\n";
            }
        }
        // 通用命令执行方法 结束

        // "切换微软电脑管家区域至中国" 功能区域 开始
        private void ChangeRegionToCN()
        {
            try
            {
                string registryPath = @"SOFTWARE\WOW6432Node\MSPCManager Store";

                // 打开注册表项，并进行删除操作
                using (RegistryKey? key = Registry.LocalMachine.OpenSubKey(registryPath, writable: true))
                {
                    if (key != null)
                    {
                        // 删除 InstallRegionCode 项（如果存在）
                        if (key.GetValue("InstallRegionCode") != null)
                        {
                            key.DeleteValue("InstallRegionCode");
                        }

                        // 创建新的 InstallRegionCode 项，并设置为 CN
                        key.SetValue("InstallRegionCode", "CN", RegistryValueKind.String);

                        ResultTextBox.Text += "区域已切换至中国。\n";
                    }
                    else
                    {
                        ResultTextBox.Text += "无法打开注册表项：未找到指定路径。\n";
                    }
                }
            }
            catch (Exception ex)
            {
                ResultTextBox.Text += $"修改注册表时出错: {ex.Message}\n";
            }
        }
        // "切换微软电脑管家区域至中国" 功能区域 结束

        // --------------------- 功能区域 结束 ---------------------

        // --------------------- "取消" 按钮功能区 开始 ---------------------
        private void CancelFeatureButton_Click(object sender, RoutedEventArgs e)
        {
            ResultTextBox.Text += "用户已取消任务。\n";
            CancelFeatureButton.IsEnabled = false;
        }
        // --------------------- "取消" 按钮功能区 结束 ---------------------

        // --------------------- "获取管家版本号" 功能区 开始 ---------------------

        // "刷新按钮" 功能区域 开始
        private void RefreshButton_Click(object sender, RoutedEventArgs e)
        {
            string? version = GetPCManagerVersion();
            if (string.IsNullOrEmpty(version))
            {
                VersionTextBlock.Text = "无法读取当前微软电脑管家版本号";
            }
            else
            {
                VersionTextBlock.Text = $"当前微软电脑管家版本号为：{version}";
            }
        }
        // "刷新按钮" 功能区域 结束

        // "读取注册表" 功能区域 开始
        private string? GetPCManagerVersion()
        {
            string? version = null;

            // 尝试从 HKLM 读取
            using (RegistryKey? key = Registry.LocalMachine.OpenSubKey(@"SOFTWARE\Microsoft\Windows\CurrentVersion\Appx\AppxAllUserStore\Applications"))
            {
                if (key != null)
                {
                    var subKeyNames = key.GetSubKeyNames().Where(name => name.Contains("Microsoft.MicrosoftPCManager_"));
                    foreach (var subKeyName in subKeyNames)
                    {
                        var parts = subKeyName.Split('_');
                        if (parts.Length > 1)
                        {
                            version = parts[1];
                            break;
                        }
                    }
                }
            }

            // 如果 HKLM 没有找到，尝试从 HKCU 读取
            if (string.IsNullOrEmpty(version))
            {
                using (RegistryKey? key = Registry.CurrentUser.OpenSubKey(@"Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\SystemAppData\Microsoft.MicrosoftPCManager_8wekyb3d8bbwe\Schemas"))
                {
                    if (key != null)
                    {
                        var packageFullName = key.GetValue("PackageFullName") as string;
                        if (!string.IsNullOrEmpty(packageFullName))
                        {
                            var parts = packageFullName.Split('_');
                            if (parts.Length > 1)
                            {
                                version = parts[1];
                            }
                        }
                    }
                }
            }

            return version;
        }
        // "读取注册表" 功能区域 结束
        // --------------------- "获取管家版本号" 功能区域 结束 ---------------------
    }
}
