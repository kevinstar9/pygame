import pygame

# 1. Pygame 초기화
pygame.init()

# 2. 화면 크기 설정 (960x640)
screen_width = 1280 
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("플레이어 이동 예제")

# 3. 프레임 속도(FPS) 설정을 위한 Clock 객체
clock = pygame.time.Clock()

# 4. 캐릭터 이미지 로드 및 설정
# 'example1.png' 파일을 불러와 player_image 변수에 저장합니다.
original_player_image = pygame.image.load('sample.png')
player_size = 128
scaled_player_image = pygame.transform.scale(original_player_image, (player_size, player_size))
# 이미지의 크기 및 위치 정보를 가진 직사각형 객체(Rect)를 가져옵니다.
player_rect = scaled_player_image.get_rect()

# Rect 객체의 중심을 화면의 중심으로 설정하여 캐릭터를 화면 중앙에 배치합니다.
player_rect.center = (screen_width // 2, screen_height // 2)

# 5. 캐릭터 이동 속도 설정
player_speed = 5

# 6. 게임 루프 설정
running = True

# 7. 메인 게임 루프
while running:
    # 게임의 초당 프레임 수(FPS)를 60으로 고정
    clock.tick(60)

    # 8. 이벤트 처리 (키 입력, 창 닫기 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False # 창 닫기 버튼을 누르면 루프 종료

    # 9. 키 입력 확인 (눌린 상태를 지속적으로 확인)
    keys = pygame.key.get_pressed()
    
    # 방향키를 누르면 Rect의 x, y 좌표를 변경하여 위치를 이동시킵니다.
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed

    # 10. 화면에 그리기
    # 배경을 검은색으로 채워 이전 프레임의 이미지를 지웁니다.
    screen.fill((0, 0, 0))

    # 화면에 플레이어 이미지를 그립니다.
    # blit() 함수는 '무엇을(이미지)' '어디에(Rect)' 그릴지 지정합니다.
    screen.blit(scaled_player_image, player_rect)

    # 11. 화면 업데이트
    pygame.display.flip()

# 12. Pygame 종료
pygame.quit()