# 👩‍🦳Speech-and-object-recognition-for-elderly-people-living-alone👨‍🦳


## 프로젝트 소개
**음성 인식과 컴퓨터 비전을 활용한 독거 노인 안부 확인 서비스**</br>
:  독거 노인들의 일상에 주기적으로 안부를 묻고, 위급한 상황 발생 시 비상 연락망으로 연락 조치할 수 있는 서비스</br>

+ 구현 동영상 </br>
https://drive.google.com/file/d/1-zyx4oHsKzfmW0_0CCX7HMN1fujugCkJ/view?usp=sharing
</br></br>

### 📅 개발 기간
2024년 5월 3주 ~ 2024년 6월 3주차
</br></br>

### ⚙ 개발 환경
![windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![mac](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)
![github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)
![git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![vscode](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![colab](https://img.shields.io/badge/Colab-F9AB00?style=for-the-badge&logo=googlecolab&color=525252)
![flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)</br>
![python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
![html](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)</br>
+ 사용한 dataset </br>
https://drive.google.com/file/d/1cejStp1n6TYp6CaD2dsXXWqUxX40c6y4/view?usp=sharing</br></br>

### 📢 OSS NOTICE

이 애플리케이션은 다음의 오픈소스 AI 모델을 포함합니다:

<details>
  <summary> <a href="https://github.com/WongKinYiu/yolov7">yolov7</a> : GNU General Public License v3.0 (GPL-3.0)</summary>

  
  #### 저작권 및 라이선스

  This application incorporates yolov7, which is licensed under the GNU General Public License v3.0 (GPL-3.0).

  Copyright © MechanIT. All rights reserved for the portions of this application that are our original work.

  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along with this program. If not, see <http://www.gnu.org/licenses/>.
</details>
<br>

+ yolov7 anaconda 가상환경
```
conda create -n yolov7 python=3.7
conda activate yolov7
conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=11.0 -c pytorch
```
+ yolov7 git clone
```
git clone https://github.com/WongKinYiu/yolov7.git
cd yolov7
pip install -r requirements.txt
```

+ 음성 출력
```
pip install gtts
pip install SpeechRecognition
pip install pyaudio
pip install pygame
pip install schedule
pip install playsound
pip install pydub 
pip install ffmpeg-python
# ffmpeg를 window에서 설치 시 별도의 설정이 필요합니다. 
# reference : https://gumu.kr/blog/1091/ffmpeg-%EC%84%A4%EC%B9%98-%EB%B0%A9%EB%B2%95/
```

+ 웹 서버
```
pip install flask
# download ngrok & execute
```

</br></br>

### 📜 flowchart
<p align="center">
<img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/project%20flowchart.png?raw=true">
</p>

</br></br>
### ✔ 주요 기능
> 1. 사람(person / fallen person) 객체 인식
> 2. person으로 객체가 인식되면 알림 음성 출력 / fallen person으로 인식되면 움직여달라는 경고 음성 출력
> 3. 위급 상황으로(fallen person으로 객체 인식되나 움직임 없을 시) 판단 시 웹페이지 출력 및 이메일 전송 </br>
</br>
<p align="center">
<img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/person%20detect.png?raw=true" height=90% width=40% />
<img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/web.png?raw=true" height=40% width=45% /> 
</p>

</br></br>
### ❓ 프로젝트 사용 방법
```
python main.py  # main.py 실행 
```
</br>

---

### 📌 Discussion

#### [ yolo 버전에 따른 한계점 비교 (pretrained model) ]
<details>
  <summary><b>yolov3 tiny</b></summary>
</br>
  <div markdown="1">
    <ul>
      <li>인식이 매우 불안정함. bounding box가 지속적으로 나타나지 않고 깜빡거림</li>
      <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/d5425817-fbd0-4613-8a26-f994f2d2bcf6" width=40%>
    </ul>
  </br>
    <ul>
      <li>누워 있는 사람의 경우, 사람으로 인지하지 못함</li>
      <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/a916836d-6226-4f9a-9d6a-21c6afcd0092" width=40%>
    </ul>
  </br>
    <ul>
      <li>정자세인 사람만 제대로 인식하며, 자세가 조금만 바뀌어도 인지하지 못함</li>
    </ul>
</details>

<details>
  <summary><b>yolov5</b></summary>
</br>
  <div markdown="1">
    <ul>
      <li>yolov3와 다르게 누워 있는 사람도 person으로 인식함.</li>
      <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/9c982336-01f1-43bb-bb86-b8f10b3be2e5" width=40%>
    </ul>
  </br>
    <ul>
    <li>객체의 일부분만 사람으로 인식하는 yolov3와 다르게, 사람(person)으로 인식하는 범위(bounding box)가 더 커지고 다양한 자세에도 사람으로 인지를 할 수 있음</li>
      <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/37b5bc68-136f-4ab9-a3ea-0e15fdcbd273" width=40%>
   </ul>
</br>
    <ul>
      <b>→ 그러나 누워 있는 자세까지 인지 불가</b>
   </ul>
</details>

<details>
  <summary><b>yolov7</b></summary>
</br>
  <div markdown="1">
    <ul>
      <li>인지 정확도가 매우 높음. 특히 사람의 경우 대부분 90% 이상의 정확도가 출력됨</li>
      <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/d9f2adcf-609b-443f-9be3-dca6db582119" width=40%>
   </ul>
</br>
</br>
    <ul>
      <li>사람이 정지해 있을 경우,  Bounding box 크기 변화가 작음</li>
      <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/c5563ec0-f5fe-4716-821e-609f3247aa28" width=40%>
   </ul>
</br>
</br>
    <ul>
      <li>yolov3, yolov5보다 실시간성이 매우 좋음</li>
   </ul>
</br>
    <ul>
        <b>→ ❗모델의 실시간성과 정확성을 고려하여, 학습시킬 모델을 yolov7으로 결정❗</b>
   </ul>
</details>

</br>

#### [ yolov9 모델 학습 문제 ]
<details>
  <summary><b>yolov9 인지 결과</b></summary>
</br>
성능비교를 위해 yolov7과  yolov9을 동일 데이터셋, 동일 batch size와 epoch로 학습을 진행함. 
</br>
그러나, yolov9 학습 모델을 실행했을 때 객체를 인지하는 비율이 낮고 인지에 성공하더라도 정확도가 아주 낮음. 
  <div markdown="1">
  </br>
    <ul>
      <li>한명이 잡혔을 때 person으로 판별가능</li>
        하드웨어의 한계상, 딜레이가 매우 심하고 person을 인지하나 그 정확도가 0.2 수준으로 낮음. 또한 거의 전신의 1/2 이상이 나와야 person으로 인지 가능하고 정자세에서 벗어나는 자세를 취하거나 거리가 가까우면 거의 인식하지 못함</br>
<img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/yolov9%20pictures/one%20person.PNG?raw=true" width=30%> 
<img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/yolov9%20pictures/close.PNG?raw=true" width=30%>
<img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/yolov9%20pictures/another%20pose.PNG?raw=true" width=30%>
    </ul>
  </br>
    <ul>
      <li>누운 사람</li>
        누운 사람의 경우, 다른 학습된 모델과 다르게 거의 인식하지 못함. 다양한 자세와 각도로 학습시켰지만 실제 검증에서는 많은 시도중에 1번 인식될 정도로 거의 인식하지 못함.</br>
         <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/yolov9%20pictures/fallen%20person.PNG?raw=true" width=30%>
    </ul>
  </br>
    <ul>
      <li>2명 이상의 사람이 화면에 나왔을 때</li>
        정상적으로 학습된 v7의 경우, 2명이 인식돼도 정확도가 떨어지지 않고 모두 사람으로 인식할 수 있는 것을 확인함. 
        </br>
        또한 2명의 자세가 달라도 동시에 성공적으로 자세를 구별하여 인식할 수 있었음.
      </br>
      </br>
        그러나 v9의 경우 2명이 화면에 나오면 각각을 person으로 인지는 하나, 2명이 각기 다른 자세를 취해도 역시 인식하지 못하고 손을 사람으로 인식하는 등 오인식 문제도 발견됨. </br>
<img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/yolov9%20pictures/two-ok.PNG?raw=true" width=30%>
<img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/blob/main/project%20pictures/yolov9%20pictures/two-not_ok.PNG?raw=true" width=30%>
</br>

</details>
<details>
   <summary><b>yolov7과 yolov9 모델 사양 비교</b></summary>
  </br>
    <ul>
      <li>yolov7과 yolov9 모델 사양의 비교</li>
      </br>
      yolov9의 경우 심한 딜레이와 낮은 인식도의 문제를 가졌음. 이를 보다 성공적이었던 yolov7과 yolov9 모델 사양의 비교를 통해 분석해봄.
      </br>
      </br>
        <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/a62149ac-f7a3-4f17-b166-fce1c5f808d0" width=80%>
      </br>
    </ul>
  </br>
    <ul>
      <li>yolov9 모델은 yolov7 모델에 비해 레이어 수가 두 배 가까이 많고, 파라미터 수와 FLOPs 또한 상당히 증가해 더 복잡하고 계산량이 많음을 의미함. 
      </br>
      </br>
          → 복잡성이 증가하면 더 많은 연산이 필요하고, 이는 더 많은 학습 데이터와 시간이 요구됨. 
      </br>
      </br>
          → 따라서 같은 조건(예: batch size, epoch)에서 학습했을 때 v7보다 yolov9 모델이 충분히 학습되지 못할 가능성이 높음.
      </li>
      </br>
      </br>
    </ul>
</details>
