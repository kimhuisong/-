import os
import sys
import pygame
import random

# 初期設定
pygame.init()

# 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("クリスマスゲーム")

# 色の設定
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 現在のスクリプトのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(current_dir, 'images')

if not os.path.exists(images_dir):
    print(f"画像ディレクトリが存在しません: {images_dir}")
    sys.exit()

# 画像の読み込み
try:
    background_image = pygame.image.load(os.path.join(images_dir, 'background.png'))
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    santa_image = pygame.image.load(os.path.join(images_dir, 'santa.png'))
    santa_image = pygame.transform.scale(santa_image, (100, 100))

    toy_image = pygame.image.load(os.path.join(images_dir, 'toy.png'))  # おもちゃ
    toy_image = pygame.transform.scale(toy_image, (50, 50))

    comic_image = pygame.image.load(os.path.join(images_dir, 'comic.png'))  # 漫画
    comic_image = pygame.transform.scale(comic_image, (50, 50))

    clothes_image = pygame.image.load(os.path.join(images_dir, 'clothes.png'))  # 洋服
    clothes_image = pygame.transform.scale(clothes_image, (50, 50))

    game_image = pygame.image.load(os.path.join(images_dir, 'game.png'))  # ゲーム
    game_image = pygame.transform.scale(game_image, (50, 50))

    # 家の画像をリストに格納
    house_images = []
    for i in range(1, 5):
        house_image = pygame.image.load(os.path.join(images_dir, f'home{i}.png'))
        house_image = pygame.transform.scale(house_image, (100, 100))
        house_images.append(house_image)
except pygame.error as e:
    print(f"画像の読み込みに失敗しました: {e}")
    sys.exit()

# サンタの位置（固定）
santa_x = 50
santa_y = screen_height // 2

# プレゼントの種類
PRESENT_TYPES = {
    "toy": toy_image,
    "comic": comic_image,
    "clothes": clothes_image,
    "game": game_image
}

# プレゼントリスト
items = []

# 家リスト
houses = []

# 日本語フォント設定
try:
    font = pygame.font.SysFont("meiryo", 24)  # meiryoフォントを使用
except:
    font = pygame.font.Font(None, 24)

# ゲーム制限時間
game_duration = 60
score = 0

# アイテムクラス
class Item:
    def __init__(self, x, y, image, item_type):
        self.x = x
        self.y = y
        self.image = image
        self.item_type = item_type
        self.velocity_x = 7
        self.velocity_y = 5

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

# 家クラス
class House:
    def __init__(self, x):
        self.x = x
        self.y = screen_height - 100
        self.image = random.choice(house_images)  # ランダムに家の画像を選択
        self.want = random.choice(list(PRESENT_TYPES.keys()))  # 欲しいプレゼントをランダムに選択

    def update(self):
        self.x -= 5

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        text = font.render(self.want, True, WHITE)  # 欲しいプレゼントを表示
        screen.blit(text, (self.x + 5, self.y - 20))

# 家の生成
def generate_house():
    max_attempts = 10
    for _ in range(max_attempts):
        new_x = screen_width
        overlap = False
        for house in houses:
            if abs(house.x - new_x) < 150:  # 距離が150未満なら重なりとみなす
                overlap = True
                break
        if not overlap:
            houses.append(House(new_x))
            break

# スタート画面
def start_screen():
    screen.fill(BLACK)
    title_text = font.render("クリスマスゲームへようこそ!", True, WHITE)
    instruction_text = font.render("欲しいプレゼントを投げて得点を稼ごう!", True, WHITE)
    start_text = font.render("Enterキーで開始", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 50))
    screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# メインゲーム
def main_game():
    global score
    start_ticks = pygame.time.get_ticks()
    running = True
    while running:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, game_duration - int(elapsed_time))

        if remaining_time <= 0:
            running = False

        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y, toy_image, "toy"))
                elif event.key == pygame.K_2:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y, comic_image, "comic"))
                elif event.key == pygame.K_3:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y, clothes_image, "clothes"))
                elif event.key == pygame.K_4:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y, game_image, "game"))

        if random.randint(0, 100) < 5:
            generate_house()

        for house in houses:
            house.update()
            house.draw(screen)

        items_to_remove = []
        houses_to_remove = []
        for item in items:
            item.update()
            item.draw(screen)

            for house in houses:
                if house.x <= item.x <= house.x + 100 and house.y <= item.y <= house.y + 100:
                    if house.want == item.item_type:
                        score += 10
                    else:
                        score -= 5
                    items_to_remove.append(item)
                    houses_to_remove.append(house)
                    break

        for item in items_to_remove:
            if item in items:
                items.remove(item)
        for house in houses_to_remove:
            if house in houses:
                houses.remove(house)

        screen.blit(santa_image, (santa_x, santa_y))

        time_text = font.render(f"Time: {remaining_time}", True, RED)
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (10, 50))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    game_over_screen()

# ゲームオーバー画面
def game_over_screen():
    screen.fill(WHITE)
    end_text = font.render("ゲーム終了！", True, RED)
    score_text = font.render(f"最終スコア: {score}", True, RED)
    restart_text = font.render("もう一度プレイするにはRキーを押してください", True, BLACK)
    screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 60))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 60))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main_game()

# 実行
start_screen()
main_game()
pygame.quit()
