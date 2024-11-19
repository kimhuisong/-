import pygame
import sys
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

# 画像の読み込み
try:
    background_image = pygame.image.load('background.png')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    santa_image = pygame.image.load('santa.png')
    santa_image = pygame.transform.scale(santa_image, (100, 100))

    present_image = pygame.image.load('present.png')
    present_image = pygame.transform.scale(present_image, (50, 50))

    potato_image = pygame.image.load('potato.jpg')  # ジャガイモ画像
    potato_image = pygame.transform.scale(potato_image, (50, 50))
except pygame.error as e:
    print(f"画像の読み込みに失敗しました: {e}")
    sys.exit()

# サンタの位置（固定）
santa_x = 50
santa_y = screen_height // 2

# プレゼントとジャガイモのリスト
items = []

# 家のリスト
houses = []

# 重力
gravity = 0.3

# 日本語フォント設定
try:
    font = pygame.font.SysFont("meiryo", 36)  # meiryoフォントを使用
except:
    font = pygame.font.Font(None, 36)  # meiryoがない場合のフォールバック

# ゲーム制限時間（60秒）
game_duration = 60  # 秒

# スコアの初期化
score = 0

# アイテム（プレゼントやジャガイモ）クラス
class Item:
    def __init__(self, x, y, image, item_type):
        self.x = x
        self.y = y
        self.image = image
        self.item_type = item_type  # "present" または "potato" を指定
        self.velocity_x = 5
        self.velocity_y = -10

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += gravity

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

# 家クラス
class House:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 50
        self.good_child = random.choice([True, False])  # 良い子か悪い子かをランダムで決定

    def update(self):
        self.x -= 5  # 家が左に移動する速度

    def draw(self, screen):
        color = (0, 0, 255) if self.good_child else (255, 0, 0)  # 良い子の家は青、悪い子の家は赤
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))

# スタート画面関数
def start_screen():
    screen.fill(BLACK)
    title_text = font.render("クリスマスゲームへようこそ!", True, WHITE)
    instruction_text = font.render("スペースキーでプレゼント、Bキーでジャガイモを投げる", True, WHITE)
    start_text = font.render("Enterキーでゲーム開始", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 50))
    screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 + 50))
    pygame.display.flip()

    # スタート画面での入力待ちループ
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enterキーでゲーム開始
                    waiting = False

# ゲームのメイン関数
def main_game():
    global score
    start_ticks = pygame.time.get_ticks()  # ゲーム開始時の時間を取得
    score = 0  # スコアのリセット
    running = True
    while running:
        # 経過時間の計算
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, game_duration - int(seconds_passed))

        # 時間が切れたらゲーム終了
        if remaining_time <= 0:
            running = False

        # 背景画像を描画
        screen.blit(background_image, (0, 0))

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # キーが押された時の処理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y + santa_image.get_height() // 2, present_image, "present"))
                elif event.key == pygame.K_b:
                    items.append(Item(santa_x + santa_image.get_width(), santa_y + santa_image.get_height() // 2, potato_image, "potato"))

        # ランダムで家を生成
        if random.randint(0, 100) < 5:
            houses.append(House(screen_width, random.randint(0, screen_height - 100)))

        # 家の更新と描画
        for house in houses:
            house.update()
            house.draw(screen)

        # アイテムの更新と描画
        items_to_remove = []
        houses_to_remove = []
        for item in items:
            item.update()
            item.draw(screen)

            # アイテムと家が重なった時の処理
            for house in houses:
                if house.x <= item.x <= house.x + house.size and house.y <= item.y <= house.y + house.size:
                    if (house.good_child and item.item_type == "present") or (not house.good_child and item.item_type == "potato"):
                        score += 10
                    else:
                        score -= 5
                    items_to_remove.append(item)
                    houses_to_remove.append(house)
                    break

        # 重複削除
        for item in items_to_remove:
            if item in items:
                items.remove(item)
        for house in houses_to_remove:
            if house in houses:
                houses.remove(house)

        # サンタの描画（固定位置）
        screen.blit(santa_image, (santa_x, santa_y))

        # 残り時間とスコアの表示
        time_text = font.render(f"Time: {remaining_time} sec", True, RED)
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (10, 50))

        # 画面の更新
        pygame.display.flip()

        # フレームレートの設定
        pygame.time.Clock().tick(60)

    game_over_screen()

# ゲーム終了画面
def game_over_screen():
    screen.fill(WHITE)
    end_text = font.render("ゲーム終了！", True, RED)
    score_text = font.render(f"最終スコア: {score}", True, RED)
    restart_text = font.render("もう一度プレイするにはRキーを押してください", True, BLACK)
    screen.blit(end_text, (screen_width // 2 - end_text.get_width() // 2, screen_height // 2 - 60))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 60))
    pygame.display.flip()

    # 再スタート待ちループ
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

# メインプログラム
start_screen()  # スタート画面を表示
main_game()      # メインゲームを開始
pygame.quit()
