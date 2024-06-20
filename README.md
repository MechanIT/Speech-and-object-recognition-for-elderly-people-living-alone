# Speech-and-object-recognition-for-elderly-people-living-alone


## 프로젝트 소개


### 📌 yolo 버전에 따른 한계점 비교 (pretrained model)
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


### 📌 yolov9 모델 학습 문제
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
        하드웨어의 한계상, 딜레이가 매우 심하고 person을 인지하나 그 정확도가 0.2 수준으로 낮음. 또한 거의 전신의 ⅔ 이상이 나와야 person으로 인지 가능하고 정자세에서 벗어나는 자세를 취하거나 거리가 가까우면 거의 인식하지 못함
    </ul>
  </br>
    <ul>
      <li>누운 사람</li>
        누운 사람의 경우, 다른 학습된 모델과 다르게 거의 인식하지 못함. 다양한 자세와 각도로 학습시켰지만 실제 검증에서는 많은 시도중에 1번 인식될 정도로 거의 인식하지 못함.
    </ul>
  </br>
    <ul>
      <li>2명 이상의 사람이 화면에 나왔을 때</li>
        정상적으로 학습된 v7의 경우, 2명이 인식돼도 정확도가 떨어지지 않고 모두 사람으로 인식할 수 있는 것을 확인함. 
        </br>
        또한 2명의 자세가 달라도 동시에 성공적으로 자세를 구별하여 인식할 수 있었음.
      </br>
      </br>
        그러나 v9의 경우 2명이 화면에 나오면 각각을 person으로 인지는 하나 2명이 각기 다른 자세를 취해도 역시 인식하지 못하고 손을 사람으로 인식하는 등 오인식 문제도 발견됨.
    </ul>
</details>
<details>
   <summary><b>yolov7과 yolov9 모델 사양 비교</b></summary>
  </br>
    <ul>
      <li>yolov7과 yolov9 모델 사양의 비교</li>
      yolov9의 경우 심한 딜레이와 낮은 인식도의 문제를 가졌음. 이를 보다 성공적이었던 yolov7과 yolov9 모델 사양의 비교를 통해 분석해봄.
      </br>
        <img src="https://github.com/MechanIT/Speech-and-object-recognition-for-elderly-people-living-alone/assets/161675231/a62149ac-f7a3-4f17-b166-fce1c5f808d0" width=80%>
      </br>
    </ul>
  </br>
    <ul>
      <li>yolov9 모델은 yolov7 모델에 비해 레이어 수가 두 배 가까이 많고, 파라미터 수와 FLOPs 또한 상당히 증가해 더 복잡하고 계산량이 많음을 의미함. 
      </br>
          복잡성이 증가하면 더 많은 연산이 필요하고, 이는 더 많은 학습 데이터와 시간이 요구됨. 
      </br>
          따라서 같은 조건(예: batch size, epoch)에서 학습했을 때 v7보다 yolov9 모델이 충분히 학습되지 못할 가능성이 높음.
      </br>
          정상적으로 학습된 v7의 경우, 2명이 인식돼도 정확도가 떨어지지 않고 모두 사람으로 인식할 수 있는 것을 확인함. 
      </br>
          또한 2명의 자세가 달라도 동시에 성공적으로 자세를 구별하여 인식할 수 있었음.
      </li>
      </br>
      </br>
    </ul>
</details>
