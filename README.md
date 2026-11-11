# G2 계산기

[https://gguntt.github.io/g2g2/](https://gguntt.github.io/g2g2/) 를 전체 화면으로 여는 안드로이드 앱입니다. 표준·공학용 계산기가 메인이고, 사이트의 환율 계산은 같은 화면 안에서 그대로 사용할 수 있습니다.

앱 이름: **G2 계산기**  
패키지: `io.github.gguntt.g2calc`

아이콘은 키패드와 주황색 등호로 계산기가 먼저 보이게 했고, 화면 속 `$ ⇄ ₩` 로 일반 계산기와 구분됩니다. 배경은 사이트의 하나·신한 색입니다.

## APK 받기

이 컴퓨터에는 안드로이드 스튜디오가 없어도 됩니다. GitHub에 올린 뒤 Actions가 APK를 만듭니다.

1. GitHub에서 새 저장소를 만듭니다. README를 자동으로 추가하지 마세요.
2. 이 폴더에서 아래를 실행합니다. 주소는 본인 저장소 주소로 바꿉니다.

```bash
git init
git add .
git commit -m "Add fullscreen calculator webview app"
git branch -M main
git remote add origin https://github.com/사용자이름/저장소이름.git
git push -u origin main
```

3. GitHub 저장소의 **Actions** 탭에서 **Build APK** 가 끝날 때까지 기다립니다. 첫 빌드는 SDK를 받아서 몇 분 걸립니다.
4. 완료된 실행을 열고, 아래 **Artifacts** 에서 `G2-calculator` 를 받습니다. 압축을 풀면 `G2-calculator.apk` 가 있습니다.
5. 휴대폰으로 APK를 옮긴 뒤 설치합니다. 설치가 막히면 설정에서 이 출처의 앱 설치를 허용하면 됩니다.

`main` 또는 `master`에 푸시할 때마다, 그리고 Actions 탭에서 **Run workflow** 를 눌러도 다시 빌드됩니다.

서명 키는 `keystore/g2calc-release.p12` 입니다. 같은 키로 서명된 APK만 기존 앱 위에 업데이트됩니다. Play 스토어에 올릴 계획이 있으면 이 키를 공개 저장소에 두지 말고, 새 키를 만들어 GitHub Secrets로 바꾸세요.
