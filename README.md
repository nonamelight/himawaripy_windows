# himawaripy (Windows 최적화 버전)
*거의 실시간으로 업데이트되는 아름다운 지구의 모습을 바탕화면으로 설정하세요!*

> **Notice:** 이 프로젝트는 [boramalper/himawaripy](https://github.com/boramalper/himawaripy)를 바탕으로 수정 및 확장하여 Windows 환경에 맞게 최적화한 버전입니다. 원본 소스코드는 MIT 라이선스를 따르며, 훌륭한 원본 프로젝트를 만들어주신 원작자에게 감사를 표합니다.

![24 hours long animation by /u/hardypart](https://i.giphy.com/l3vRnMYNnbhdnz5Ty.gif)

## 🎉 Windows 전용 신기능 안내
기존 리눅스 환경에 특화되어있던 기능을 대폭 개선하여, **컴퓨터를 잘 모르는 분들도 윈도우에서 손쉽게 사용할 수 있도록** 만들어졌습니다! `HimawariPy.exe`를 통해 단 한 번의 클릭으로 모든 기능을 사용할 수 있습니다.

### 주요 기능
- **시스템 트레이 완벽 지원**: 검은색 콘솔 창 없이 시스템 트레이(작업 표시줄 우측 하단)에 상주하며 알아서 바탕화면을 업데이트해 줍니다.
- **윈도우 시작 시 자동 실행**: `HimawariPy.exe`를 한 번 실행해두면, 다음부터는 컴퓨터(윈도우)를 켤 때마다 자동으로 켜져서 백그라운드에서 동작합니다. (설정 창에서 켜고 끌 수 있습니다)
- **실시간 과거 시간 여행 (Time Travel)**: `Settings` 메뉴에서 슬라이드바를 조작한 후 마우스를 놓으면 즉각적으로 과거의 지구 모습을 미리보고 바탕화면으로 설정할 수 있습니다. 
- **자동 시간 흐름 연동**: 과거 시점을 지정해두면, 그 시점으로부터 계속해서 시간이 흘러가며 다음 사진으로 업데이트됩니다!
- **화면 크기 완벽 맞춤 (Scaling)**: 지구가 너무 크게 보이는 것을 방지하기 위해 `Earth Scale` 비율을 조절할 수 있습니다. 윈도우 바탕화면 설정과 무관하게 언제나 정중앙에 깔끔하게 맞춤 배치됩니다.
- **쉬운 업데이트 주기 설정**: 복잡한 스케줄러(cron) 설정 없이 GUI 화면에서 분 단위로 직관적인 설정이 가능합니다.

---

## Linux 및 Mac OS 사용자 매뉴얼
*주의: 위에서 소개한 GUI(설정 창) 및 트레이 기능은 윈도우(Windows) 전용 기능이며, Linux/Mac OS의 경우 기존 방식(cronjob 등) 그대로 충돌 없이 완벽히 호환되어 동작합니다.*

himawaripy는 [Himawari 8 (ひまわり8号)](https://en.wikipedia.org/wiki/Himawari_8) 위성이 촬영한 10분 지연된 실시간 지구 사진을 가져와 바탕화면으로 설정하는 Python 3 스크립트입니다. 
주기적으로 바탕화면을 갱신하려면 매 10분마다 실행되는 cronjob(혹은 systemd 서비스)을 설정하세요.

### 지원하는 데스크탑 환경 (Linux/Mac)
#### 테스트 완료
* Unity 7
* Mate 1.8.1
* Pantheon
* LXDE
* OS X
* GNOME 3
* Cinnamon 2.8.8
* KDE

#### 미지원
* 위에 언급되지 않은 다른 데스크탑 환경

## 설정 (CLI)

```
usage: himawaripy [-h] [--version] [--auto-offset | -o OFFSET]
                  [-l {4,8,16,20}] [-d DEADLINE] [--save-battery]
                  [--output-dir OUTPUT_DIR] [--dont-change]

set (near-realtime) picture of Earth as your desktop background

optional arguments:
  -h, --help            이 도움말 메시지를 표시하고 종료합니다
  --version             프로그램 버전을 표시하고 종료합니다
  --auto-offset         자동으로 시간대를 계산합니다
  -o OFFSET, --offset OFFSET
                        UTC 시간대 오프셋 (시간), +10 이하의 값이어야 합니다
  -l {4,8,16,20}, --level {4,8,16,20}
                        타일의 품질(및 크기)을 높입니다. 4, 8, 16, 20 사용 가능
  -d DEADLINE, --deadline DEADLINE
                        모든 타일을 다운로드하는 데 걸리는 제한 시간(분), 0으로 설정하면 제한 해제
  --save-battery        배터리 사용 시 새로고침을 중지합니다
  --output-dir OUTPUT_DIR
                        임시 바탕화면 이미지를 저장할 디렉토리
  --dont-change         바탕화면을 변경하지 않습니다 (다운로드만 수행)
```

대부분의 경우 `--auto-offset` 플래그를 넘겨주면 시간대를 정확히 감지할 수 있지만, `-o` (또는 `--offset`) 플래그로 수동 설정할 수도 있습니다. 시간대가 GMT 기준으로 10시간 이상 차이난다면, 가장 가까운 값(`+10` 또는 `-12`)을 사용하세요.

level을 높이면 이미지 품질이 좋아지지만 모든 타일을 다운로드하는 시간과 메모리 사용량이 증가합니다. 예를 들어 20을 선택하면 최대 약 700 MiB의 메모리를 사용하고 약 200 MB 크기의 이미지가 생성됩니다.

스크립트가 다시 시작되기 전에 종료될 수 있도록 cronjob(또는 타이머) 설정과 호환되는 다운로드 제한 시간(deadline)을 지정하는 것이 좋습니다.

랩톱 배터리로 실행 중일 때 새로고침을 비활성화하려면 `--save-battery` 옵션을 사용할 수 있습니다.

이미지만 다운로드하고 바탕화면은 변경하지 않으려면 `--dont-change` 플래그를 사용하세요.

### Nitrogen
바탕화면 설정에 nitrogen을 사용하는 경우, `~/.config/nitrogen/bg-saved.cfg` 파일에 다음 내용을 추가해야 합니다.

```
[:0.0]
file=/home/USERNAME/.himawari/himawari-latest.png
mode=4
bgcolor=#000000
```

## 설치 (Linux/Mac)
* python3-setuptools 패키지가 포함된 유효한 python3 설치 환경이 필요합니다.

```
# 설치
python3 -m pip install --user himawaripy

# 작동 테스트
himawaripy --auto-offset

# 제공된 systemd 타이머를 사용하여 주기적으로 himawaripy가 실행되도록 설정
    ## systemd 구성 복사 (bash 기준)
    cp systemd/himawaripy.{service,timer} ~/.config/systemd/user/

    ## 타이머 활성화 및 시작
    systemctl --user enable --now himawaripy.timer
```

### KDE 사용자 대상
#### KDE 5.7 이상
KDE 5.7+에서 바탕화면을 변경하려면 데스크탑 위젯 잠금을 해제해야 합니다. 잠금 해제를 원치 않으시면 이전 버전(Pre-KDE 5.7)의 방법을 사용할 수 있습니다.

데스크탑 위젯 잠금 해제 방법 ([KDE userbase 참고](https://userbase.kde.org/Plasma#Widgets)):
> Desktop Toolbox나 Panel Toolbox를 열거나 데스크탑 우클릭 후 'Unlock Widgets' 항목을 선택합니다. 그 다음 데스크탑이나 패널에 위젯을 추가할 수 있습니다.

#### KDE 5.7 이전 버전
> 핵심은 KDE가 커맨드라인을 통한 바탕화면 변경을 지원하지 않지만, "슬라이드쇼" 배경화면 옵션을 통해 폴더의 파일 변경을 감지하고 주기적으로 새 사진을 불러오는 것은 지원한다는 점입니다.
>
> 1. 특정 주기(예: 9분)로 cron을 설정합니다.
> 2. Desktop Settings -> Wallpaper -> Wallpaper Type -> Slideshow 로 이동합니다.
> 3. 슬라이드쇼 목록에 `~/.himawari` 디렉토리를 추가합니다.
> 4. 주기(interval check)를 10분으로 설정합니다. (다운로드 속도에 따라 cron 설정보다 1분 뒤로 설정)

훌륭한 해결책을 찾아주신 [xenithorb](https://github.com/xenithorb/himawaripy/commit/01d7c681ae7ce47f639672733d0f734574662833) 님께 감사드립니다!

### Mac OSX 사용자 대상
OSX는 crontab을 더 이상 사용하지 않으며 `launchd`로 대체했습니다. launch agent를 설정하려면 제공된 `osx/org.boramalper.himawaripy.plist` 샘플 파일을 `~/Library/LaunchAgents`에 복사하고 필요한 경우 수정하세요.

    mkdir -p ~/Library/LaunchAgents/
    cp osx/org.boramalper.himawaripy.plist ~/Library/LaunchAgents/

* `ProgrammingArguments`는 himawaripy 설치 경로여야 합니다. 기본적으로 `/usr/local/bin/himawaripy`를 가리키지만, 다른 위치에 설치되었을 수 있습니다.
* `StartInterval`은 연속 실행 사이의 간격을 제어합니다. 기본값은 10분(600초)이며 원하는 대로 편집하세요.

마지막으로 실행하려면 콘솔에 다음을 입력하세요.

    launchctl load ~/Library/LaunchAgents/org.boramalper.himawaripy.plist


## 삭제

```
# 1. cronjob 제거
crontab -e
    # 아래 라인 삭제
    */10 * * * * himawaripy...

# 2. 또는 systemd 타이머를 사용한 경우
systemctl --user disable --now himawaripy.timer
rm $HOME/.config/systemd/user/himawaripy.{timer,service}

# 3. 패키지 삭제
pip3 uninstall himawaripy
```

`<INSTALLATION_PATH>`는 `which -- himawaripy` 명령을 통해 찾을 수 있습니다.

## Attributions
초기 Powershell 스크립트 [구현](https://gist.github.com/MichaelPote/92fa6e65eacf26219022)을 도와주신 *[MichaelPote](https://github.com/MichaelPote)* 님께 감사드립니다.

이미지 처리 로직([hi8-fetch.py](https://gist.github.com/celoyd/39c53f824daef7d363db))을 작성해주신 *[Charlie Loyd](https://github.com/celoyd)* 님께 감사드립니다.

이 사진들을 대중에게 공개해주신 일본 기상청(Japan Meteorological Agency)에도 깊은 감사를 표합니다.

---

# himawaripy (Windows Optimized Version)
*Put a near-realtime picture of Earth as your desktop background!*

> **Notice:** This project is a fork of [boramalper/himawaripy](https://github.com/boramalper/himawaripy), modified and extended to be optimized for Windows environments. The original source code is under the MIT License, and we express our gratitude to the original author for creating such an amazing project.

![24 hours long animation by /u/hardypart](https://i.giphy.com/l3vRnMYNnbhdnz5Ty.gif)

## 🎉 New Features for Windows
The original features, heavily specialized for Linux, have been greatly improved so that **even non-technical users can easily use it on Windows!** With `HimawariPy.exe`, you can access all features with a single click.

### Key Features
- **Full System Tray Support**: It resides in the system tray (bottom right of the taskbar) without any black console windows, automatically updating your wallpaper.
- **Run at Windows Startup**: Run `HimawariPy.exe` just once, and it will automatically register itself to run in the background every time you turn on your PC. (Can be toggled in Settings)
- **Real-time Time Travel**: By adjusting the slider in the `Settings` menu, you can instantly preview and set the Earth's appearance up to 24 hours in the past.
- **Automatic Time Flow**: If you set a past time, time will naturally continue to flow from that point, automatically updating to the next picture!
- **Perfect Screen Scaling**: To prevent the Earth from appearing too large, you can adjust the `Earth Scale` percentage. It will always be perfectly centered, regardless of your Windows wallpaper settings.
- **Easy Update Interval Setup**: You can intuitively set the update interval in minutes right from the GUI, without complex scheduler (cron) configurations.

---

## Linux and Mac OS User Manual
*Note: The GUI (Settings window) and tray features introduced above are exclusive to Windows. On Linux/Mac OS, the traditional methods (like cronjobs) will continue to work perfectly without any conflicts.*

himawaripy is a Python 3 script that fetches near-realtime (10 minutes delayed) picture of Earth as its taken by [Himawari 8 (ひまわり8号)](https://en.wikipedia.org/wiki/Himawari_8) and sets it as your desktop background.

Set a cronjob (or systemd service) that runs in every 10 minutes to automatically get the near-realtime picture of Earth.

### Supported Desktop Environments (Linux/Mac)
#### Tested
* Unity 7
* Mate 1.8.1
* Pantheon
* LXDE
* OS X
* GNOME 3
* Cinnamon 2.8.8
* KDE

#### Not Supported
* any other desktop environments that are not mentioned above.

## Configuration (CLI)

```
usage: himawaripy [-h] [--version] [--auto-offset | -o OFFSET]
                  [-l {4,8,16,20}] [-d DEADLINE] [--save-battery]
                  [--output-dir OUTPUT_DIR] [--dont-change]

set (near-realtime) picture of Earth as your desktop background

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --auto-offset         determine offset automatically
  -o OFFSET, --offset OFFSET
                        UTC time offset in hours, must be less than or equal
                        to +10
  -l {4,8,16,20}, --level {4,8,16,20}
                        increases the quality (and the size) of each tile.
                        possible values are 4, 8, 16, 20
  -d DEADLINE, --deadline DEADLINE
                        deadline in minutes to download all the tiles, set 0
                        to cancel
  --save-battery        stop refreshing on battery
  --output-dir OUTPUT_DIR
                        directory to save the temporary background image
  --dont-change         don't change the wallpaper (just download it)
```

Most of the time himawaripy can accurately detect your timezone if you pass the flag `--auto-offset`, although you may also set it manually by `-o` (or `--offset`) flag. If your timezone is beyond GMT by more than 10 hours, use the closest one (either `+10` or `-12`).

Increasing the level will increase the quality of the image as well as the time taken to download all the tiles and the memory consumption. For instance choosing 20 will make himawaripy use ~700 MiB of memory at its peak and the image will be around ~200 MB.

You should set a deadline compatible with your cronjob (or timer) settings to assure that script will terminate in X minutes before it is started again.

You might use `--save-battery` to disable refreshing while running on battery power.

You might also ask himawaripy to not to change your wallpaper by `--dont-change` if you would like it to download the image and stop.

### Nitrogen
If you use nitrogen for setting your wallpaper, you have to enter this in your `~/.config/nitrogen/bg-saved.cfg`.

```
[:0.0]
file=/home/USERNAME/.himawari/himawari-latest.png
mode=4
bgcolor=#000000
```

## Installation (Linux/Mac)
* You need a valid python3 installation including the python3-setuptools package.

```
# Install
python3 -m pip install --user himawaripy

# Test whether it's working
himawaripy --auto-offset

# Set himawaripy to be called periodically using the provided systemd timer
    ## Copy systemd configuration (on bash)
    cp systemd/himawaripy.{service,timer} ~/.config/systemd/user/

    ## Enable and start the timer
    systemctl --user enable --now himawaripy.timer
```

### For KDE Users
#### KDE 5.7+
To change the wallpaper in KDE 5.7+, desktop widgets must be unlocked. If you don't want to leave them unlocked, the pre-KDE 5.7 method can still be used.

To unlock desktop widgets ([from the KDE userbase](https://userbase.kde.org/Plasma#Widgets)):
> Open the Desktop Toolbox or the Panel Toolbox or right click on the Desktop - if you see an item labeled Unlock Widgets then select that, and then proceed to add widgets to your Desktop or your Panel.

#### Before KDE 5.7
> So the issue here is that KDE does not support changing the desktop wallpaper from the commandline, but it does support polling a directory for file changes through the "Slideshow" desktop background option, whereby you can point KDE to a folder and have it load a new picture at a certain interval.
>
> The idea here is to:
>
> * Set the cron for some interval (say 9 minutes)
> * Open Desktop Settings -> Wallpaper -> Wallpaper Type -> Slideshow
> * Add the `~/.himawari` dir to the slideshow list
> * Set the interval check to 10 minutes (one minute after the cron, also depending on your download speed)

Many thanks to [xenithorb](https://github.com/xenithorb) [for the solution](https://github.com/xenithorb/himawaripy/commit/01d7c681ae7ce47f639672733d0f734574662833)!

### For Mac OSX Users

OSX has deprecated crontab, and replaced it with `launchd`. To set up a launch agent, copy the provided sample `plist` file in `osx/org.boramalper.himawaripy.plist` to `~/Library/LaunchAgents`, and edit the following entries if required.

    mkdir -p ~/Library/LaunchAgents/
    cp osx/org.boramalper.himawaripy.plist ~/Library/LaunchAgents/

* `ProgrammingArguments` needs to be the path to himawaripy installation. This *should* be `/usr/local/bin/himawaripy` by default, but himawaripy may be installed elsewhere.

* `StartInterval` controls the interval between successive runs, set to 10 minutes (600 seconds) by default, edit as desired.

Finally, to launch it, enter this into the console:

    launchctl load ~/Library/LaunchAgents/org.boramalper.himawaripy.plist


## Uninstallation

```
# 1. Either remove the cronjob
crontab -e
    # Remove the line
    */10 * * * * himawaripy...

# 2. OR if you used the systemd timer
systemctl --user disable --now himawaripy.timer
rm $HOME/.config/systemd/user/himawaripy.{timer,service}

# 3. Uninstall the package
pip3 uninstall himawaripy
```

`<INSTALLATION_PATH>` can be found using the command `which -- himawaripy`.

## Attributions
Thanks to *[MichaelPote](https://github.com/MichaelPote)* for the [initial implementation](https://gist.github.com/MichaelPote/92fa6e65eacf26219022) using Powershell Script.

Thanks to *[Charlie Loyd](https://github.com/celoyd)* for image processing logic ([hi8-fetch.py](https://gist.github.com/celoyd/39c53f824daef7d363db)).

Obviously, thanks to the Japan Meteorological Agency for opening these pictures to public.
