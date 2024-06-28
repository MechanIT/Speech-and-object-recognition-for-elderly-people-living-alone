# Speech-and-object-recognition-for-elderly-people-living-alone

## 📌 프로젝트 소개
독거 노인이 홀로 생활하다가 갑자기 쓰러질 경우, 이를 인지하여 위급 상황임을 비상연락망으로 알리는 시스템을 구축하고자 한다. 


사람이 쓰러져 있는 모습을 웹캠과 yolo를 통한 컴퓨터 비전을 사용하여 인식하고자 한다.


기본 yolo 학습 모델은 사람은 인식할 수 있으나, 사람이 누워 있는 자세는 인식하지 못한다. 


따라서 누워 있는 사람과 서 있는 사람을 구분할 수 있는 데이터셋을 직접 제작하고 yolov7에 학습시켜, 쓰러진 사람을 인식할 수 있는 딥러닝 모델을 만들었다.


## 📌 yolov7 모델 사용


**사용한 custom dataset 다운로드 링크 : https://drive.google.com/file/d/1cejStp1n6TYp6CaD2dsXXWqUxX40c6y4/view?usp=sharing**


**학습된 weight 파일 다운로드 링크 : [https://drive.google.com/file/d/1TxBgH3QAgy9GKMBtFIzrcpQZuciRXTmR/view?usp=sharing](https://drive.google.com/file/d/1ideXUrj1fqiu3NaD1xfzMq_eik1AqVll/view?usp=sharing)**


## 📌 실행 방법
1. weight 파일 다운로드
2. yolov7 github 전체 코드 다운로드 (링크 : https://github.com/WongKinYiu/yolov7/tree/main)
3. 아나콘다 가상환경 설정

		conda create -n yolov7_env python=3.7.13
		conda activate yolov7_env
		pip install -r "yolov7 코드 다운 받은 경로\yolov7\requirements.txt"
   		
5. yolov7 코드 다운 받은 경로로 weight 파일 옮기기, 이 경로에서 다음 명령어 실행
		
		python detect.py --weights best_final.pt --conf 0.25 --img-size 640 --source 0



## 📌 학습 과정

### 📌yolov7을 통한 custom dataset 학습

1. 학습을 위해 GPU가 필요하므로, colab 환경에서 진행
   런타임 유형 GPU로 설정

- colab 링크 : https://colab.research.google.com/drive/1ayfBCIIm9Y-SSkFzCzBfIuJn3eZd7eod?usp=sharing

2. yolov7 다운로드
   	!git clone https://github.com/WongKinYiu/yolov7.git 	// yolov7 다운로드


3. 관련 라이브러리 설치
	
	 	%cd yolov7 //생성된 yolov7 폴더로 이동
		pip install -r requirements.txt	//yolov7 실행에 필요한 라이브러리 설치

4. dataset 압축 해제

   		%cd /content/dataset
		!unzip /content/drive/MyDrive/dataset_for_oss_final.zip

6. /content/data.yaml 파일은 다음과 같이 설정

		train : /content/dataset/dataset_for_oss/train/images	//자신의 경로에 맞게 수정
		val : /content/dataset/dataset_for_oss/valid/images

		nc : 2
		names: ['person', 'fallen person']


7. dataset 안에 있는 yolov7-custom.yaml 파일을 yolov7>cfg>training 폴더에 옮기기


- /content/yolov7/cfg/training/yolov7-custom.yaml 파일은 다음과 같이 설정


	--> yolov7.yaml 파일에서 class number만 수정함

		# parameters
		nc: 2  # number of classes
		depth_multiple: 1.0  # model depth multiple
		width_multiple: 1.0  # layer channel multiple


7. yolov7 학습

		%cd /content/yolov7
		!python train.py --batch-size 8 --epochs 30 --img 640 480  --data /content/dataset/dataset_for_oss/data.yaml --cfg /content/yolov7/cfg/training/yolov7-custom.yaml --name yolov7_for_oss --weights yolov7.pt	








