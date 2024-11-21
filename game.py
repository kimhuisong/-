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
music_dir = os.path.join(current_dir,'music')

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

#BGMの読み込み
try:
    pygame.mixer.music.load(os.path.join(music_dir, 'jinglebell.wav'))
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"効果音の読み込みに失敗しました: {e}")
    sys.exit()

#効果音の読み込み
try:
    present_sound = pygame.mixer.Sound(os.path.join(music_dir,'throw.wav'))
except pygame.error as e:
    print(f"効果音の読み込みに失敗しました: {e}")
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

# スタート画面用の背景画像を読み込み
try:
    start_background_image = pygame.image.load(os.path.join(images_dir, 'start_background.png'))
    # 背景画像を画面サイズにフィットさせるようにスケーリング
    bg_width, bg_height = start_background_image.get_size()
    scale_ratio = min(screen_width / bg_width, screen_height / bg_height) * 1.2
    new_width = int(bg_width * scale_ratio)
    new_height = int(bg_height * scale_ratio)
    start_background_image = pygame.transform.scale(start_background_image, (new_width, new_height))

    start_santa_image = pygame.image.load(os.path.join(images_dir,'start_santa.png'))
    start_santa_image = pygame.transform.scale(start_santa_image, (screen_width, screen_height))
except pygame.error as e:
    print(f"スタート画面用背景画像の読み込みに失敗しました: {e}")
    sys.exit()

# スタート画面
def start_screen():
    # 背景画像の描画
    bg_width, bg_height = start_background_image.get_size()
    bg_x = (screen_width - bg_width) // 2
    bg_y = (screen_height - bg_height) // 2
    screen.blit(start_background_image, (bg_x, bg_y))

    screen.blit(start_santa_image, (0,0))
    # 説明文のリスト
    instructions = [
        "ゲームの遊び方:",
        "1. 欲しいプレゼントを家に届けよう",
        "2. 各プレゼントに対応するキーを投げよう",
        "        - 1: おもちゃ",
        "        - 2: 漫画",
        "        - 3: 洋服",
        "        - 4: ゲーム",
        "3. 制限時間: 60秒",
    ]
    text_y = screen_height // 2 - 150  # 白い部分の中央を基準に調整
    for line in instructions:
        text = font.render(line, True, BLACK)  # 黒文字で描画
        screen.blit(text, (300, text_y))
        text_y += 30  # 行間を空ける
    start_text = font.render("Enterキーで開始", True, RED)
    screen.blit(start_text, (400, text_y + 20))

    # 描画を反映
    pygame.display.flip()

    # 入力待ちループ
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enterキーでゲーム開始
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
                    present_sound.play()
                elif event.key == pygame.K_2:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y, comic_image, "comic"))
                    present_sound.play()
                elif event.key == pygame.K_3:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y, clothes_image, "clothes"))
                    present_sound.play()
                elif event.key == pygame.K_4:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y, game_image, "game"))
                    present_sound.play()

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
