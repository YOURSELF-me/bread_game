import pygame
import random
import time

pygame.init()
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))  # 가로와 세로의 길이를 튜플 형태로 넣어줌.

pygame.display.set_caption("빵돌이의_오븐대작전 game")
total_score = 0  # 점수
clock = pygame.time.Clock()  # 나중에 프레임 설정을 위해 넣음.
level_control = 18  # 게임 시작할때 반죽덩어리의 갯수
game_font = pygame.font.Font(None, 35)  # 점수표시를 위한 글꼴설정1
game_font1 = pygame.font.Font(None, 45)  # 점수표시를 위한 글꼴설정2
large_font = pygame.font.Font(None, 40)

background = pygame.image.load("배경.png")
mySound = pygame.mixer.Sound("빵돌이 배경음악 (Click Clock).mp3")

player = pygame.image.load("프로틴빵돌이.png")
player_size = player.get_rect().size  # 이미지의 크기를 구해옴
player_width = player_size[0]  # 플레이어의 가로 크기
player_height = player_size[1]  # 플레이어의 세로 크기
player_x_pos = (screen_width / 2) - (player_width / 2)
player_y_pos = (screen_height / 2) - (player_height / 2)

player_to_x = 0  # 이동할 때 사용하는 임시 변수
player_to_y = 0
player_speed = 0.3  # player 스피드 설정

item = pygame.image.load("프로틴.png")
item_size = item.get_rect().size
item_width = item_size[0]
item_height = item_size[1]
item_x_pos = random.randint(0, screen_width - player_width)
item_y_pos = -2000
item_speed = 4

strongerTime = 10  # 무적끝나는 시간
strongerMode = False  # 무적모드
strongerStartTime = 0  # 무적시작 시간

feverImage = pygame.image.load("fever바 모형.png")
feverImages = []
feverImages.append(pygame.image.load("fever바1.png"))

enemy_list = list()  # 장애물을 생성할 때 enemy_list라는 리스트에 enemy_class의 객체를 하나씩 담는다.  만약 장애물이 맵 밖으로 나간 경우, 해당 객체를 리스트에서 삭제시키면 됨.

class enemy_class:  # 장애물에 대한 정보가 담겨 있는 클래스
    enemy_image = pygame.image.load("반죽덩어리.png")
    enemy_size = enemy_image.get_rect().size  # 이미지 크기 저장
    enemy_width = enemy_size[0]
    enemy_height = enemy_size[1]
    enemy_spawnPoint = None  # 장애물의 스폰 지점을 결정할 값
    enemy_x_pos = 0  # 장애물의 x,y좌표를 가지는 값
    enemy_y_pos = 0
    enemy_rad = 0  # 장애물이 스폰된 후, 각도가 30도 방향, 45도 방향,90도 방향 중 어느 각도로 이동할 것인지 정하는 값

    enemy_rect = enemy_image.get_rect()  # 충돌 판정을 확인하기 위한 정보
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    def __init__(self):  # 여기부터 생성자 부분, 여기에서 랜덤으로 스폰 위치, 각도를 정함
        self.enemy_spawnPoint = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])  # 위, 아래, 왼쪽, 오른쪽 중 어디에서 스폰될 것인지 정함.
        # 장애물은 화면 밖에서 생성되어 화면 안을 지나가기 위한 준비코드이다.

        # 스폰 지점 설정
        if self.enemy_spawnPoint == 'LEFT':
            self.enemy_x_pos = - self.enemy_width
            self.enemy_y_pos = random.randint(0, screen_height - self.enemy_height)
            self.enemy_rad = random.choice(
                [(1, 3), (1, 2), (2, 2), (2, 1), (3, 1), (3, 0), (1, -3), (1, -2), (2, -2), (2, -1), (3, -1)])
        elif self.enemy_spawnPoint == 'RIGHT':
            self.enemy_x_pos = screen_width
            self.enemy_y_pos = random.randint(0, screen_height - self.enemy_height)
            self.enemy_rad = random.choice(
                [(-1, 3), (-1, 2), (-2, 2), (-2, 1), (-3, 1), (-3, 0), (-1, -3), (-1, -2), (-2, -2), (-2, -1),
                 (-3, -1)])
        elif self.enemy_spawnPoint == 'UP':
            self.enemy_x_pos = random.randint(0, screen_width - self.enemy_width)
            self.enemy_y_pos = - self.enemy_height
            self.enemy_rad = random.choice(
                [(3, 1), (2, 1), (2, 2), (1, 2), (1, 3), (0, 3), (-3, 1), (-2, 1), (-2, 2), (-1, 2), (-1, 3)])
        elif self.enemy_spawnPoint == 'DOWN':
            self.enemy_x_pos = random.randint(0, screen_width - self.enemy_width)
            self.enemy_y_pos = screen_height
            self.enemy_rad = random.choice(
                [(3, -1), (2, -1), (2, -2), (1, -2), (1, -3), (0, -3), (-3, -1), (-2, -1), (-2, -2), (-1, -2),
                 (-1, -3)])

    def enemy_move(self):
        self.enemy_x_pos += self.enemy_rad[0]
        self.enemy_y_pos += self.enemy_rad[1]
        global total_score

        def boundary_UP():  # 상하좌우로 화면을 넘어갔는지 아닌지 확인
            if self.enemy_y_pos < -self.enemy_height:
                return True

        def boundary_DOWN():
            if self.enemy_y_pos > screen_height:
                return True

        def boundary_LEFT():
            if self.enemy_x_pos < -self.enemy_width:
                return True

        def boundary_RIGHT():
            if self.enemy_x_pos > screen_width:
                return True

        if self.enemy_spawnPoint == 'UP':  # 해당 화면을 넘어갔다면 객체를 지워버림.
            if boundary_LEFT() or boundary_RIGHT() or boundary_DOWN():
                enemy_list.remove(self)
                total_score += 1

        if self.enemy_spawnPoint == 'DOWN':
            if boundary_LEFT() or boundary_RIGHT() or boundary_UP():
                enemy_list.remove(self)
                total_score += 1

        if self.enemy_spawnPoint == 'LEFT':
            if boundary_UP() or boundary_DOWN() or boundary_RIGHT():
                enemy_list.remove(self)
                total_score += 1

        if self.enemy_spawnPoint == 'RIGHT':
            if boundary_UP() or boundary_DOWN() or boundary_LEFT():
                enemy_list.remove(self)
                total_score += 1

    def enemy_coll(self):  # 충돌 판정을 위해 enemy_rect를 최신화
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_rect.left = self.enemy_x_pos
        self.enemy_rect.top = self.enemy_y_pos



running = True

while running:
    mySound.play(-1)
    dt = clock.tick(60)  # 1초에 60프레임

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 프로그램의 끄기버튼(x버튼)을 눌렀을 때 running = False 루프 종료
            running = False

        if event.type == pygame.KEYDOWN:  # KEYDOWN : 키보드를 눌렀을 때
            if event.key == pygame.K_LEFT:  # 방향키를 눌렀을 때 해당 방향에 x,y좌표 값을 더함.
                player_to_x -= player_speed
            if event.key == pygame.K_RIGHT:
                player_to_x += player_speed
            if event.key == pygame.K_UP:
                player_to_y -= player_speed
            if event.key == pygame.K_DOWN:
                player_to_y += player_speed

        if event.type == pygame.KEYUP:  # 키보드에서 손을 땠을 때 x,y 추가값 초기화
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_to_x = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player_to_y = 0

    player_x_pos += player_to_x * dt
    player_y_pos += player_to_y * dt

    # 프로틴(아이템)이 떨어지도록
    if item_y_pos > screen_height:
        item_y_pos = -2000
        item_x_pos = random.randint(0, screen_width - item_width)
    item_y_pos += item_speed

    # 프로틴빵돌이(캐릭터) 경계값 : 플레이어의 캐릭터가 화면 밖으로 나가지 못하게 해주는 코드
    if player_x_pos < 0:
        player_x_pos = 0
    elif player_x_pos > screen_width - player_width:
        player_x_pos = screen_width - player_width
    if player_y_pos < 0:
        player_y_pos = 0
    elif player_y_pos > screen_height - player_height:
        player_y_pos = screen_height - player_height

    if level_control >= len(enemy_list):
        enemy_list.append(enemy_class())

    # 충돌 처리
    player_rect = player.get_rect()
    player_rect.left = player_x_pos
    player_rect.top = player_y_pos

    # 아이템 먹기
    item_rect = item.get_rect()
    item_rect.left = item_x_pos
    item_rect.top = item_y_pos
    fever = 0

    # 무적상태 체크
    if strongerMode and time.time() - strongerStartTime > strongerTime:
        player = pygame.image.load("프로틴빵돌이.png")
        strongerMode = False

    if player_rect.colliderect(item_rect):
        item_y_pos = -8000
        item_x_pos = random.randint(0, screen_width - item_width)
        fever += 1
        if fever == 1:
            strongerMode = True
            strongerStartTime = time.time()
            player = pygame.image.load("fever빵돌이1.png")

    for i in enemy_list:  # enemy_list 리스트 안에 있는 모든 enemy_class()객체의 rect정보를 최신화함.
        i.enemy_coll()
        if player_rect.colliderect(i.enemy_rect):
            if strongerMode:  # 무적상태인 경우, 장애물과 충돌해도 10초간 무적
                strongerMode = True
            else:  # 무적상태가 아닌 경우, 장애물과 충돌시 게임 종료.
                strongerMode = False
                running = False

    # 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(player, (player_x_pos, player_y_pos))
    screen.blit(item, (item_x_pos, item_y_pos))

    for i in enemy_list:
        i.enemy_move()
        screen.blit(i.enemy_image, (i.enemy_x_pos, i.enemy_y_pos))
    score = game_font.render('Score: ' + str(int(total_score)), True, (51, 51, 51))
    screen.blit(score, (screen_width - 140, 15))

    #-------------------------------
    screen.blit(feverImage, (35, 20))
    if strongerMode == True:
        screen.blit(feverImages[0], (35, 20))
        if time.time() - strongerStartTime > 6 and time.time() - strongerStartTime <= 10:
            feverImages[0], feverImage = feverImage, feverImages[0]
            if time.time() - strongerStartTime > 10:
                strongerMode = False
                screen.blit(feverImage, (35, 20))

    for i in enemy_list:
        if player_rect.colliderect(i.enemy_rect) and strongerMode == False:
            game_result = "* GAME OVER *"
            gameOver_background = pygame.image.load("게임오버 배경.png")
            gameOver_background_size = gameOver_background.get_rect().size
            gameOver_background_width = gameOver_background_size[0]
            gameOver_background_height = gameOver_background_size[1]
            gameOver_background_x_pos = (screen_width / 2) - (player_width / 2)
            gameOver_background_y_pos = (screen_height / 2) - (player_height / 2)
            screen.blit(gameOver_background, (120, 175))

            msg = game_font.render(game_result, True, (0, 0, 0))
            msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2) - 100))
            screen.blit(msg, msg_rect)

            point_result = game_font1.render('Score: ' + str(int(total_score)), True, (200,38,0))
            point_result_rect = point_result.get_rect(center=(int(screen_width / 2), int(screen_height / 2) - 20))
            screen.blit(point_result, point_result_rect)

            if total_score > 1111:
                grade_result = game_font1.render('Grade: A+', True, (200, 38, 0))
                grade_result_rect = grade_result.get_rect(center=(int(screen_width / 2), int(screen_height / 2) + 40))
                screen.blit(grade_result, grade_result_rect)
            elif total_score > 700:
                grade_result1 = game_font1.render('Grade: A', True, (200, 38, 0))
                grade_result_rect1 = grade_result1.get_rect(center=(int(screen_width / 2), int(screen_height / 2) + 40))
                screen.blit(grade_result1, grade_result_rect1)
            elif total_score > 500:
                grade_result2 = game_font1.render('Grade: B', True, (200, 38, 0))
                grade_result_rect2 = grade_result2.get_rect(center=(int(screen_width / 2), int(screen_height / 2) + 40))
                screen.blit(grade_result2, grade_result_rect2)
            elif total_score > 300:
                grade_result3 = game_font1.render('Grade: C', True, (200, 38, 0))
                grade_result_rect3 = grade_result3.get_rect(center=(int(screen_width / 2), int(screen_height / 2) + 40))
                screen.blit(grade_result3, grade_result_rect3)
            elif total_score > 150:
                grade_result4 = game_font1.render('Grade: D', True, (200, 38, 0))
                grade_result_rect4 = grade_result4.get_rect(center=(int(screen_width / 2), int(screen_height / 2) + 40))
                screen.blit(grade_result4, grade_result_rect4)
            else:
                grade_result5 = game_font1.render('Grade: F', True, (200, 38, 0))
                grade_result_rect5 = grade_result5.get_rect(center=(int(screen_width / 2), int(screen_height / 2) + 40))
                screen.blit(grade_result5, grade_result_rect5)

            pygame.display.update()
            pygame.time.wait(3000)
    pygame.display.update()
pygame.quit()
크하하
