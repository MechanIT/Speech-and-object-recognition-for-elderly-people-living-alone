# Speech-and-object-recognition-for-elderly-people-living-alone

## yolov7 모델 사용


사용한 dataset : https://drive.google.com/file/d/1cejStp1n6TYp6CaD2dsXXWqUxX40c6y4/view?usp=sharing


학습된 weight 파일 : [https://drive.google.com/file/d/1TxBgH3QAgy9GKMBtFIzrcpQZuciRXTmR/view?usp=sharing](https://drive.google.com/file/d/1ideXUrj1fqiu3NaD1xfzMq_eik1AqVll/view?usp=sharing)


실행 방법
1. weight 파일 다운로드
2. yolov7 github 전체 코드 다운로드 (링크 : https://github.com/WongKinYiu/yolov7/tree/main)
3. 아나콘다 가상환경 설정
		conda create -n yolov7_env python=3.7.13
		conda activate yolov7_env
		pip install -r "yolov7 코드 다운 받은 경로\yolov7\requirements.txt"
   		
5. yolov7 코드 다운 받은 경로로 weight 파일 옮기기, 이 경로에서 다음 명령어 실행
		
		python detect.py --weights best_final.pt --conf 0.25 --img-size 640 --source 0

## 프로젝트 소개
독거 노인이 홀로 생활하다가 갑자기 쓰러질 경우, 이를 인지하여 위급 상황임을 비상연락망으로 알리는 시스템을 구축하고자 한다. 


사람이 쓰러져 있는 모습을 웹캠과 yolo를 통한 컴퓨터 비전을 사용하여 인식하고자 한다.


기본 yolo 학습 모델은 사람은 인식할 수 있으나, 사람이 누워 있는 자세는 인식하지 못한다. 


따라서 누워 있는 사람과 서 있는 사람을 구분할 수 있는 데이터셋인 FPDS 데이터셋을 yolov7에 학습시켜, 쓰러진 사람을 인식할 수 있는 딥러닝 모델을 만들었다.


FPDS 데이터셋 : <https://gram.web.uah.es/data/datasets/fpds/index.html>


## 진행 과정

###  📌using pretrained weight file


#### 1. weight files 다운로드

FPDS 웹페이지에 yolov3으로 학습시킨 weight파일 존재, 이를 다운로드



#### 2. 원래 코드에서 weight 파일만 바꿔서 실행했으나, 사람 아예 인식 불가

→ 아예 다른 방법으로 진행

→ Darknet 상에서 yolo와 weigth파일을 설정해서 실행 가능한 것으로 보임



#### 3. Darknet을 통한 객체 인식

yolov3을 사용하기 위한 Darknet 환경설정 참고자료 : https://kd1658.tistory.com/23


웹캠 yolov3 테스트 참고자료 : https://kd1658.tistory.com/25




<Darknet 실행 과정>


1. CUDA v12.5 설치


	* 경로 C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5


2. cuDNN v8.9.7 설치


	* https://developer.nvidia.com/rdp/cudnn-archive


	* 압축파일 풀고 안에 있는 파일 4개를 CUDA 경로에 복사


3. OpenCV 설치


	* 경로  C:\opencv


4. Darknet 설치


	* https://github.com/AlexeyAB/darknet


	* 경로 C:\darknet-master


5. Darknet 빌드


	* https://m.blog.naver.com/estern/221828977313


	  **-> 지속적으로 빌드 에러가 발생하여, 포기하고 모델을 새로 학습하기로 결정!!**




### 📌yolov7을 통한 FPDS dataset 학습

1. 학습을 위해 GPU가 필요하므로, colab 환경에서 진행

![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/6b842115-d05f-45e4-97b3-ae5d82c55a4d)


2. yolov7 다운로드
   	!git clone https://github.com/WongKinYiu/yolov7.git 	// yolov7 다운로드


3. 관련 라이브러리 설치
	
	 	%cd yolov7 //생성된 yolov7 폴더로 이동
		pip install -r requirements.txt	//yolov7 실행에 필요한 라이브러리 설치


4. /content/data.yaml 파일 작성

		train : /content/train_for_oss/train_for_oss_sep/images
		val : /content/valid_for_oss/valid_for_oss_sep/images
		
		nc : 2
		names: ['-1', '1']


5. /content/yolov7/cfg/training/yolov7-custom.yaml 파일 작성


	--> yolov7.yaml 파일에서 class number만 수정

		# parameters
		nc: 2  # number of classes
		depth_multiple: 1.0  # model depth multiple
		width_multiple: 1.0  # layer channel multiple

6. yolov7 학습

		%cd /content/yolov7
		!python train.py --batch-size 8 --epochs 30 --img 640 480  --data /content/data.yaml --cfg /content/yolov7/cfg/training/yolov7-custom.yaml --name yolov7_for_oss --weights yolov7.pt	



가은 72
문정 75
세영 134
지수 101
총 382

306 train, 76 validation 8:2



**<드라이브 옮길 때 수정사항>**

1. backup 계정에 있는 yolov7 사본 생성
2. 드라이브에 dataset_for_oss.zip 파일 올리기
3. /content 아래에 dataset 폴더 생성
4. dataset 폴더에서 zip파일 압축 해제
5. dataset 안에 있는 yolov7-custom.yaml 파일을 yolov7>cfg>training 폴더에 옮기기
6. dataset 안에 있는 data.yaml 파일에서 train, val 폴더 경로 수정
   
		 train : /content/dataset/dataset_for_oss/train/images
		 val : /content/dataset/dataset_for_oss/valid/images
		 
		 nc : 2
		 names: ['person', 'fallen person']
	

