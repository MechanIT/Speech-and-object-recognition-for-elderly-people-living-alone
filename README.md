# Speech-and-object-recognition-for-elderly-people-living-alone


## 프로젝트 소개
독거 노인이 홀로 생활하다가 갑자기 쓰러질 경우, 이를 인지하여 위급 상황임을 비상연락망으로 알리는 시스템을 구축하고자 한다. 


사람이 쓰러져 있는 모습을 웹캠과 yolo를 통한 컴퓨터 비전을 사용하여 인식하고자 한다.


기본 yolo 학습 모델은 사람은 인식할 수 있으나, 사람이 누워 있는 자세는 인식하지 못한다. 


따라서 누워 있는 사람과 서 있는 사람을 구분할 수 있는 데이터셋인 FPDS 데이터셋을 yolov7에 학습시켜, 쓰러진 사람을 인식할 수 있는 딥러닝 모델을 만들었다.


FPDS 데이터셋 : <https://gram.web.uah.es/data/datasets/fpds/index.html>


## 진행 과정

###  😂using pretrained weight file


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


	* -> 지속적으로 빌드 에러가 발생하여, 포기하고 모델을 새로 학습하기로 결정!!




### 😂yolov7을 통한 FPDS dataset 학습

* 학습을 위해 GPU가 필요하므로, colab 환경에서 진행

![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/6b842115-d05f-45e4-97b3-ae5d82c55a4d)


* yolov7 다운로드	
 	!git clone https://github.com/WongKinYiu/yolov7.git 	// yolov7 다운로드

![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/d15293c1-8e27-4f0d-b233-b948fd59477f)


* 관련 라이브러리 설치
	%cd yolov7 //생성된 yolov7 폴더로 이동
	pip install -r requirements.txt	//yolov7 실행에 필요한 라이브러리 설치

![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/38881cbf-64a9-444b-ab34-660e1bd34e49)


* data.yaml 파일 작성

	train : /content/drive/MyDrive/train_for_oss
	val : /content/drive/MyDrive/valid_for_oss
	
	nc : 2
	names: ['-1', '1']


* yolov7-custom.yaml 파일 작성

yolov7.yaml 파일에서 class number만 수정

	# parameters
	nc: 2  # number of classes
	depth_multiple: 1.0  # model depth multiple
	width_multiple: 1.0  # layer channel multiple
	
	# anchors
	anchors:
	  - [12,16, 19,36, 40,28]  # P3/8
	  - [36,75, 76,55, 72,146]  # P4/16
	  - [142,110, 192,243, 459,401]  # P5/32
	
	# yolov7 backbone
	backbone:
	  # [from, number, module, args]
	  [[-1, 1, Conv, [32, 3, 1]],  # 0
	  
	   [-1, 1, Conv, [64, 3, 2]],  # 1-P1/2      
	   [-1, 1, Conv, [64, 3, 1]],
	   
	   [-1, 1, Conv, [128, 3, 2]],  # 3-P2/4  
	   [-1, 1, Conv, [64, 1, 1]],
	   [-2, 1, Conv, [64, 1, 1]],
	   [-1, 1, Conv, [64, 3, 1]],
	   [-1, 1, Conv, [64, 3, 1]],
	   [-1, 1, Conv, [64, 3, 1]],
	   [-1, 1, Conv, [64, 3, 1]],
	   [[-1, -3, -5, -6], 1, Concat, [1]],
	   [-1, 1, Conv, [256, 1, 1]],  # 11
	         
	   [-1, 1, MP, []],
	   [-1, 1, Conv, [128, 1, 1]],
	   [-3, 1, Conv, [128, 1, 1]],
	   [-1, 1, Conv, [128, 3, 2]],
	   [[-1, -3], 1, Concat, [1]],  # 16-P3/8  
	   [-1, 1, Conv, [128, 1, 1]],
	   [-2, 1, Conv, [128, 1, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [[-1, -3, -5, -6], 1, Concat, [1]],
	   [-1, 1, Conv, [512, 1, 1]],  # 24
	         
	   [-1, 1, MP, []],
	   [-1, 1, Conv, [256, 1, 1]],
	   [-3, 1, Conv, [256, 1, 1]],
	   [-1, 1, Conv, [256, 3, 2]],
	   [[-1, -3], 1, Concat, [1]],  # 29-P4/16  
	   [-1, 1, Conv, [256, 1, 1]],
	   [-2, 1, Conv, [256, 1, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [[-1, -3, -5, -6], 1, Concat, [1]],
	   [-1, 1, Conv, [1024, 1, 1]],  # 37
	         
	   [-1, 1, MP, []],
	   [-1, 1, Conv, [512, 1, 1]],
	   [-3, 1, Conv, [512, 1, 1]],
	   [-1, 1, Conv, [512, 3, 2]],
	   [[-1, -3], 1, Concat, [1]],  # 42-P5/32  
	   [-1, 1, Conv, [256, 1, 1]],
	   [-2, 1, Conv, [256, 1, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [[-1, -3, -5, -6], 1, Concat, [1]],
	   [-1, 1, Conv, [1024, 1, 1]],  # 50
	  ]
	
	# yolov7 head
	head:
	  [[-1, 1, SPPCSPC, [512]], # 51
	  
	   [-1, 1, Conv, [256, 1, 1]],
	   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
	   [37, 1, Conv, [256, 1, 1]], # route backbone P4
	   [[-1, -2], 1, Concat, [1]],
	   
	   [-1, 1, Conv, [256, 1, 1]],
	   [-2, 1, Conv, [256, 1, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [[-1, -2, -3, -4, -5, -6], 1, Concat, [1]],
	   [-1, 1, Conv, [256, 1, 1]], # 63
	   
	   [-1, 1, Conv, [128, 1, 1]],
	   [-1, 1, nn.Upsample, [None, 2, 'nearest']],
	   [24, 1, Conv, [128, 1, 1]], # route backbone P3
	   [[-1, -2], 1, Concat, [1]],
	   
	   [-1, 1, Conv, [128, 1, 1]],
	   [-2, 1, Conv, [128, 1, 1]],
	   [-1, 1, Conv, [64, 3, 1]],
	   [-1, 1, Conv, [64, 3, 1]],
	   [-1, 1, Conv, [64, 3, 1]],
	   [-1, 1, Conv, [64, 3, 1]],
	   [[-1, -2, -3, -4, -5, -6], 1, Concat, [1]],
	   [-1, 1, Conv, [128, 1, 1]], # 75
	      
	   [-1, 1, MP, []],
	   [-1, 1, Conv, [128, 1, 1]],
	   [-3, 1, Conv, [128, 1, 1]],
	   [-1, 1, Conv, [128, 3, 2]],
	   [[-1, -3, 63], 1, Concat, [1]],
	   
	   [-1, 1, Conv, [256, 1, 1]],
	   [-2, 1, Conv, [256, 1, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [-1, 1, Conv, [128, 3, 1]],
	   [[-1, -2, -3, -4, -5, -6], 1, Concat, [1]],
	   [-1, 1, Conv, [256, 1, 1]], # 88
	      
	   [-1, 1, MP, []],
	   [-1, 1, Conv, [256, 1, 1]],
	   [-3, 1, Conv, [256, 1, 1]],
	   [-1, 1, Conv, [256, 3, 2]],
	   [[-1, -3, 51], 1, Concat, [1]],
	   
	   [-1, 1, Conv, [512, 1, 1]],
	   [-2, 1, Conv, [512, 1, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [-1, 1, Conv, [256, 3, 1]],
	   [[-1, -2, -3, -4, -5, -6], 1, Concat, [1]],
	   [-1, 1, Conv, [512, 1, 1]], # 101
	   
	   [75, 1, RepConv, [256, 3, 1]],
	   [88, 1, RepConv, [512, 3, 1]],
	   [101, 1, RepConv, [1024, 3, 1]],
	
	   [[102,103,104], 1, IDetect, [nc, anchors]],   # Detect(P3, P4, P5)
	  ]

