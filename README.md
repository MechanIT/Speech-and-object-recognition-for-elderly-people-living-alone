# Speech-and-object-recognition-for-elderly-people-living-alone




https://gram.web.uah.es/data/datasets/fpds/index.html
FPDS 데이터셋 : 누워 있는 사람과 서 있는 사람을 구분할 수 있는 데이터셋

[진행 과정]
weight files 다운로드
E-FPDS (Code + Annotations) 다운로드
→ FPDS_info 폴더 안에 여러 파일 존재. 별 내용 아닌듯
E-FPDS (Script for visualization of annotations. The script must be run in the directory where you desire to visualize annotations). 코드 실행해보고자 함
→ 라벨링 어쩌구 하길래 라벨링 관련 내용 있는 줄 알았음. 근데 알고보니 이미지 하나씩 보면서 라벨링 하는 코드였음
→ 실행해보려고 했는데 여러 모듈 다운받아야 해서 포기함. 할 필요도 없을 듯

(gi 다운받으려면 PyGObject 설치해야 한대서, 이를 설치 중 에러 발생)
(yolo_test) C:\Users\cdsl>pip3 install PyGObject
Collecting PyGObject
  Downloading pygobject-3.48.2.tar.gz (715 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 715.2/715.2 kB 1.7 MB/s eta 0:00:00
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Installing backend dependencies ... done
  Preparing metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error

  × Preparing metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [25 lines of output]
      + meson setup C:\Users\cdsl\AppData\Local\Temp\pip-install-53b_am02\pygobject_e4ffd54a8015415abcffccdea0d5cead C:\Users\cdsl\AppData\Local\Temp\pip-install-53b_am02\pygobject_e4ffd54a8015415abcffccdea0d5cead\.mesonpy-2iebsb_9 -Dbuildtype=release -Db_ndebug=if-release -Db_vscrt=md -Dtests=false -Dwheel=true --wrap-mode=nofallback --native-file=C:\Users\cdsl\AppData\Local\Temp\pip-install-53b_am02\pygobject_e4ffd54a8015415abcffccdea0d5cead\.mesonpy-2iebsb_9\meson-python-native-file.ini
      The Meson build system
      Version: 1.4.0
      Source dir: C:\Users\cdsl\AppData\Local\Temp\pip-install-53b_am02\pygobject_e4ffd54a8015415abcffccdea0d5cead
      Build dir: C:\Users\cdsl\AppData\Local\Temp\pip-install-53b_am02\pygobject_e4ffd54a8015415abcffccdea0d5cead\.mesonpy-2iebsb_9
      Build type: native build
      Project name: pygobject
      Project version: 3.48.2
      Activating VS 17.9.2
      C compiler for the host machine: cl (msvc 19.39.33521 "Microsoft (R) C/C++ 최적화 컴파일러 버전 19.39.33521(x64)")
      C linker for the host machine: link link 14.39.33521.0
      Host machine cpu family: x86_64
      Host machine cpu: x86_64
      Program python3 found: YES (C:\Users\cdsl\anaconda3\envs\yolo_test\python.exe)
      Run-time dependency python found: YES 3.11
      Did not find pkg-config by name 'pkg-config'
      Found pkg-config: NO
      Found CMake: C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin\cmake.EXE (3.28.0)
      Run-time dependency gobject-introspection-1.0 found: NO (tried pkgconfig and cmake)
      Not looking for a fallback subproject for the dependency gobject-introspection-1.0 because:
      Use of fallback dependencies is disabled.

      ..\meson.build:29:9: ERROR: Dependency 'gobject-introspection-1.0' is required but not found.

      A full log can be found at C:\Users\cdsl\AppData\Local\Temp\pip-install-53b_am02\pygobject_e4ffd54a8015415abcffccdea0d5cead\.mesonpy-2iebsb_9\meson-logs\meson-log.txt
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.

원래 코드에서 weight 파일만 바꿔서 실행했으나, 사람 아예 인식 불가

→ 아예 다른 방법으로 진행
→ Darknet 상에서 yolo와 weigth파일을 설정해서 실행 가능한 듯으로 보임


yolov3을 사용하기 위한 Darknet 환경설정 https://kd1658.tistory.com/23
웹캠 yolov3 테스트 https://kd1658.tistory.com/25

Darknet 실행

CUDA v12.5 설치
경로 C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5

cuDNN v8.9.7 설치
https://developer.nvidia.com/rdp/cudnn-archive
압축파일 풀고 안에 있는 파일 4개를 CUDA 경로에 복사

OpenCV 설치
경로  C:\opencv

Darknet 설치
https://github.com/AlexeyAB/darknet
경로 C:\darknet-master

Darknet 빌드
https://m.blog.naver.com/estern/221828977313
Visual Studio 설정은 위 블로그가 한글로 되어 있어 이를 따름.

처음엔 cudnn 관련 에러 발생
→ cudnn 제대로 설치 후 CUDA 폴더에 넣어주니 해결


C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\include 관련 에러


VC++ 디렉터리
https://m.blog.naver.com/estern/221828977313
여기서 수정하라함

시도 1)
포함 디렉터리
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\include;C:\opencv\opencv\build\include;

라이브러리 디렉터리
C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\lib\x64;C:\opencv\opencv\build\x64\vc15\lib;

시도 2)
포함 디렉터리
$(VC_IncludePath);$(WindowsSDK_IncludePath);C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\include;C:\opencv\opencv\build\include;

라이브러리 디렉터리
$(VC_LibraryPath_x64);$(WindowsSDK_LibraryPath_x64);C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\lib\x64;C:\opencv\opencv\build\x64\vc15\lib;

→ 암만 만져봐도 해결 안되어서 default로 진행
<default>
$(VC_IncludePath);$(WindowsSDK_IncludePath);

$(VC_LibraryPath_x64);$(WindowsSDK_LibraryPath_x64);


C/C++, 링커
https://kd1658.tistory.com/23
여기서는 opencv 경로만 추가하라고 함
https://wjs7347.tistory.com/m/4
여기서는 opencv, CUDA 경로 모두 추가하라고 함

<디폴트값>
C/C++>일반>추가 포함 디렉터리

$(OPENCV_DIR)\include;C:\opencv_3.0\opencv\build\include;..\..\include;..\..\3rdparty\stb\include;..\..\3rdparty\pthreads\include;%(AdditionalIncludeDirectories);$(CudaToolkitIncludeDir);$(CUDNN)\include;$(cudnn)\include;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5;


링커>일반>추가 라이브러리 디렉터리
$(OPENCV_DIR)\x64\vc15\lib;$(OPENCV_DIR)\x64\vc14\lib;$(CUDA_PATH)\lib\$(PlatformName);$(CUDNN)\lib\x64;$(cudnn)\lib\x64;..\..\3rdparty\pthreads\lib;%(AdditionalLibraryDirectories);C:\opencv\opencv\build\x64\vc15\lib;

→ 이런식으로 opencv vc15, vc14가 섞여 있음… 하나로 통일해야 할 듯


시도 1) opencv, CUDA 추가하고 쓸데없어보이는거 (OPENCV_DIR_ 삭제

추가 포함 디렉터리

C:\opencv\opencv\build\include;..\..\include;..\..\3rdparty\stb\include;..\..\3rdparty\pthreads\include;%(AdditionalIncludeDirectories);$(CudaToolkitIncludeDir);C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5;


추가 라이브러리 디렉터리	$(CUDA_PATH)\lib\$(PlatformName);$(cudnn)\lib\x64;..\..\3rdparty\pthreads\lib;%(AdditionalLibraryDirectories);C:\opencv\opencv\build\x64\vc15\lib;

	시도 2) opencv만 추가
	
추가 포함 디렉터리	C:\opencv\opencv\build\include;..\..\include;..\..\3rdparty\stb\include;..\..\3rdparty\pthreads\include;%(AdditionalIncludeDirectories);

추가 라이브러리 디렉터리	
$(cudnn)\lib\x64;..\..\3rdparty\pthreads\lib;%(AdditionalLibraryDirectories);C:\opencv\opencv\build\x64\vc15\lib;

시도 3) Opencv 추가 부분을 뒷부분으로

..\..\include;..\..\3rdparty\stb\include;..\..\3rdparty\pthreads\include;%(AdditionalIncludeDirectories);C:\opencv\opencv\build\include;

$(cudnn)\lib\x64;..\..\3rdparty\pthreads\lib;%(AdditionalLibraryDirectories);C:\opencv\opencv\build\x64\vc15\lib;

시도 4) CUDA 경로 뒷부분에 추가
..\..\include;..\..\3rdparty\stb\include;..\..\3rdparty\pthreads\include;%(AdditionalIncludeDirectories);C:\opencv\opencv\build\include;$(CudaToolkitIncludeDir);$(cudnn)\include;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5;

$(cudnn)\lib\x64;..\..\3rdparty\pthreads\lib;%(AdditionalLibraryDirectories);C:\opencv\opencv\build\x64\vc15\lib;C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\lib\x64;



처음부터 다시 확인
https://jjjhong.tistory.com/24
→ GPU가 있는 노트북에서 실행해야 할 듯
→ 버전도 위 링크랑 동일하게 진행하기
Visual Studio 2015
CUDA 9.0
cuDNN 7.6.5
OpenCV 4.0.1


플랫폼 도구 집합의 VS 버전과 darknet.vcxproj 의 ToolsVersion이 같은지 확인


→ Visual Studio 2015년 버전으로 설치 필요할 듯
	

