# Speech-and-object-recognition-for-elderly-people-living-alone
## 프로젝트 소개
**음성 인식과 컴퓨터 비전을 활용한 독거 노인 안부 확인 서비스**</br>
:  독거 노인들의 일상에 주기적으로 안부를 묻고, 위급한 상황 발생 시 비상 연락망으로 연락 조치할 수 있는 서비스</br>

+ 구현 동영상 </br>
https://drive.google.com/file/d/1-zyx4oHsKzfmW0_0CCX7HMN1fujugCkJ/view?usp=sharing
</br></br>

### yolov9 시도
-> https://yunwoong.tistory.com/319 <br/> <br/> 

사용한 dataset : https://drive.google.com/file/d/1cejStp1n6TYp6CaD2dsXXWqUxX40c6y4/view?usp=sharing <br/> 
best.pt 파일 : 

### flask / webSocket을 이용한 webpage cam streaming 
-> Flask (Python 웹 프레임워크): Python 백엔드를 구성하는 데 사용됩니다. <br/> 

-> HTML5 및 JavaScript: 프론트엔드를 구성하고 웹 페이지에서 카메라를 제어하는 데 사용됩니다.<br/> 
https://keepworking.tistory.com/28<br/> 

-> WebSocket: 클라이언트와 서버 간의 실시간 양방향 통신을 위해 사용됩니다.<br/> 



+ yolov9 anaconda 가상환경
```
conda create -n yolov7 python=3.7
conda activate yolov7
conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=11.0 -c pytorch
```
+ yolov9 git clone
```
git clone https://github.com/WongKinYiu/yolov7.git
cd yolov7
pip install -r requirements.txt
```


### ❓ 프로젝트 사용 방법
```
python main.py  # main.py 실행 
```


