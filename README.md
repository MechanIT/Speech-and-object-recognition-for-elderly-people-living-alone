# Speech-and-object-recognition-for-elderly-people-living-alone


## 프로젝트 소개


## yolo 버전에 따른 한계점 비교 (pretrained model)

### 📌 yolov3 tiny
- 인식이 매우 불안정함. bounding box가 지속적으로 나타나지 않고 깜빡거림
  ![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/d5425817-fbd0-4613-8a26-f994f2d2bcf6)



- 누워 있는 사람의 경우, 사람으로 인지하지 못함
  
  ![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/a916836d-6226-4f9a-9d6a-21c6afcd0092)



- 정자세인 사람만 제대로 인식하며, 자세가 조금만 바뀌어도 인지하지 못함


### 📌 yolov5
- v3와 다르게 누워 있는 사람도 person으로 인식함.
  ![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/9c982336-01f1-43bb-bb86-b8f10b3be2e5)



- 객체의 일부분만 사람으로 인식하는 v3와 다르게, 사람(person)으로 인식하는 범위(bounding box)가 더 커지고 다양한 자세에도 사람으로 인지를 할 수 있음

  ![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/37b5bc68-136f-4ab9-a3ea-0e15fdcbd273)



- 그러나 누워 있는 자세까지 인지 불가


  
### 📌 yolov7
- 인지 정확도가 매우 높음. 특히 사람의 경우 대부분 90% 이상의 정확도가 출력됨

  ![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/d9f2adcf-609b-443f-9be3-dca6db582119)


- 사람이 정지해 있을 경우,  Bounding box 크기 변화가 작음

  ![image](https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/c5563ec0-f5fe-4716-821e-609f3247aa28)


- yolov3, yolov5보다 실시간성이 매우 좋음
	→ 모델의 실시간성과 정확성을 고려하여, 학습시킬 모델을 yolov7으로 결정
