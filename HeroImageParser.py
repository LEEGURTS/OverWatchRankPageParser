import numpy as np
import cv2
import glob
import sys
import collections
from skimage.metrics import structural_similarity as compare_ssim

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

heroNameList = ['겐지','둠피스트','디바','라인하르트','레킹볼','로드호그','루시우',
                '리퍼','메르시','메이','모이라','바스티온','바티스트','브리기테',
                '소전','솔저','솜브라','시그마','시메트라','아나','애쉬','에코'
                ,'오리사','위도우메이커','윈스턴','자리야','정커퀸','정크렛'
                ,'젠야타','캐서디','키리코','토르비온','트레이서','파라','한조']

img_files = glob.glob('.\\CapturedImage\\*.png')

if not img_files:
    print("png 이미지를 넣어주세용..")
    sys.exit()

heroImageList = []

for heroName in heroNameList:
    tempImage = imread(f"./HeroImage/{heroName}.png")
    tempImage = cv2.resize(tempImage,dsize=(50,50),interpolation=cv2.INTER_AREA)
    tempImage = cv2.cvtColor(tempImage,cv2.COLOR_BGR2GRAY)
    heroImageList.append(tempImage)

firstPos = [1306,300]
imageSize = 50
rowGap = 2
colGap = 5

heroCounter = collections.defaultdict(int)

for captureImagePath in img_files:
    captureImage = imread(captureImagePath)
    captureImage = cv2.cvtColor(captureImage,cv2.COLOR_BGR2GRAY)
    for row in range(3):
        for col in range(10):
            sim = 0
            heroName = ""
            selectedImage = captureImage[300 + col*imageSize + col*colGap : 300 + (col+1)*imageSize + col*colGap,
                            1306 + row*imageSize + row*rowGap: 1306 + (row+1)*imageSize + row*rowGap]

            for idx,heroImage in enumerate(heroImageList):
                (score, diff) = compare_ssim(heroImage, selectedImage, full=True)
                if score > sim:
                    sim = score
                    heroName = heroNameList[idx]

            heroCounter[heroName]+=1

print(heroCounter)

input("종료하려면 아무키나 눌러주세요.")

cv2.waitKey()
cv2.destroyAllWindows()