# Speech-and-object-recognition-for-elderly-people-living-alone

## 프로젝트 소개
**음성 인식과 컴퓨터 비전을 활용한 독거 노인 안부 확인 서비스**</br>
:  독거 노인들의 일상에 주기적으로 안부를 묻고, 위급한 상황 발생 시 비상 연락망으로 연락 조치할 수 있는 서비스</br>

+ 구현 동영상 </br>
https://drive.google.com/file/d/1-zyx4oHsKzfmW0_0CCX7HMN1fujugCkJ/view?usp=sharing
</br></br>

### ✔ yolov9 시도
+ 사용한 dataset : https://drive.google.com/file/d/1B8vn-ZE4BRU-bZZGA5LAEsHwdrj0j7gb/view?usp=sharing <br/> 
+ best.pt(weight) 파일 : https://drive.google.com/file/d/1FYmHv_5HWLFQeh-Dzu5Ea2OS7civYXJR/view?usp=sharing
+ colab 학습 : yolov9_final.ipynb  <br/> 

+ yolov9 anaconda 가상환경
```
anaconda 가상환경(python=3.10.13)
CUDA=11.4
cudnn=8.5
pytorch=1.12.0
torchvision=0.13.0
```
+ yolov9 git clone
```
git clone https://github.com/WongKinYiu/yolov9
cd yolov9
pip install -r requirements.txt
```


### ❓ 프로젝트 사용 방법
```
python detect_dual.py --device 0 --weights best.pt (자신이 설정한 weight파일 경로)
```

#### ➕ camera streaming 웹페이지 출력
```
# Node.js를 설치
node main.js
```



