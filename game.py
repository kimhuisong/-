import os
import sys
import pygame
import math
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
    santa_image = pygame.transform.scale(santa_image, (200, 200))

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
santa_y = 200


# プレゼントの種類
PRESENT_TYPES = {
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

# サンタの回転動作に関する変数
santa_rotation_angle = 0  # 現在の回転角度
santa_is_throwing = False  # サンタが投げ動作中かどうか
throw_start_time = 0  # 投げ動作の開始時間

# アイテムクラス
class Item:
    def __init__(self, x, y, image, item_type, angle=-50, speed=10):
        self.x = x
        self.y = y
        self.image = image
        self.item_type = item_type

        # 投げる角度と速度を基に水平・垂直速度を計算
        self.velocity_x = speed * math.cos(math.radians(angle))
        self.velocity_y = -speed * math.sin(math.radians(angle))

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))

# 家クラス
class House:
    def __init__(self, x):
        self.x = x
        self.y = screen_height - 90
        self.image = random.choice(house_images)  # ランダムに家の画像を選択
        self.want = random.choice(list(PRESENT_TYPES.keys()))  # 欲しいプレゼントをランダムに選択

    def update(self):
        self.x -= 3

    def draw(self, screen):
        # 家の画像を描画
        screen.blit(self.image, (self.x, self.y))

        # 吹き出しの描画
        bubble_width = 60
        bubble_height = 60
        bubble_x = self.x + self.image.get_width() // 2 - bubble_width // 2
        bubble_y = self.y - bubble_height - 10
        pygame.draw.ellipse(screen, WHITE, (bubble_x, bubble_y, bubble_width, bubble_height))
        pygame.draw.ellipse(screen, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2)

        # 欲しいプレゼントの画像を吹き出し内に描画
        want_image = PRESENT_TYPES[self.want]
        want_image_scaled = pygame.transform.scale(want_image, (40, 40))
        screen.blit(want_image_scaled, (bubble_x + 10, bubble_y + 10))

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

# スコアランキングファイル
score_file = os.path.join(current_dir, "scores.txt")

def load_scores():
    if not os.path.exists(score_file):
        return []
    with open(score_file, "r") as f:
        scores = []
        for line in f.readlines():
            parts = line.strip().split(":")
            if len(parts) == 2:  # データが "name:score" の形式であるかを確認
                name, score = parts
                try:
                    scores.append((name, int(score)))
                except ValueError:
                    continue  # スコアが整数でない場合はスキップ
        return scores


# スコアランキングの保存
def save_scores(new_score):
    scores = load_scores()
    scores.append(("Player", new_score))  # 仮の名前として "Player" を使用
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[:5]  # トップ5を保持
    with open(score_file, "w") as f:
        for name, score in scores:
            f.write(f"{name}:{score}\n")


def start_screen():
    # 1. ランキング表示ページ
    show_ranking_screen()

    # 2. 遊び方説明ページ
    show_instructions_screen()

def show_ranking_screen():
    # 背景画像の描画
    bg_width, bg_height = start_background_image.get_size()
    bg_x = (screen_width - bg_width) // 2
    bg_y = (screen_height - bg_height) // 2
    screen.blit(start_background_image, (bg_x, bg_y))

    # ランキングの表示
    scores = load_scores()
    title_text = font.render("ランキング", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

    rank_text_y = screen_height // 4 + 50
    for rank, (name, score) in enumerate(scores, 1):
        rank_line = f"{rank}. {name} - {score} 点"
        text = font.render(rank_line, True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, rank_text_y))
        rank_text_y += 40

    next_text = font.render("スペースキーで次へ進む", True, WHITE)
    screen.blit(next_text, (screen_width // 2 - next_text.get_width() // 2, screen_height - 150))

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
                if event.key == pygame.K_SPACE:  # スペースキーで次に進む
                    waiting = False

def show_instructions_screen():
    # 背景画像の描画
    bg_width, bg_height = start_background_image.get_size()
    bg_x = (screen_width - bg_width) // 2
    bg_y = (screen_height - bg_height) // 2
    screen.blit(start_background_image, (bg_x, bg_y))

    # 「ゲームの遊び方」のタイトル
    title_font = pygame.font.SysFont("meiryo", 50, bold=True)  # 大きなフォント
    title_text = title_font.render("ゲームの遊び方", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 8))

    # 説明文のリスト（中央寄せ用）
    instructions = [
        "1. 欲しいプレゼントを家に届けよう",
        "2. 各プレゼントに対応するキーを投げよう",
    ]

    # プレゼント選択肢
    options = [
        ("- 1: ゲーム", game_image),
        ("- 2: 洋服", clothes_image),
        ("- 3: 漫画", comic_image),
    ]

    # 説明文の描画（中央寄せ）
    text_y = screen_height // 4
    font_to_use = pygame.font.SysFont("meiryo", 24)  # 通常サイズの白フォント
    for line in instructions:
        text = font_to_use.render(line, True, WHITE)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, text_y))
        text_y += 50

    # 選択肢の描画
    for line, image in options:
        text = font_to_use.render(line, True, WHITE)
        text_x = screen_width // 2 - text.get_width() // 2
        screen.blit(text, (text_x, text_y))

        # 画像をテキストの右に配置
        image_scaled = pygame.transform.scale(image, (50, 50))
        screen.blit(image_scaled, (text_x + text.get_width() + 20, text_y - 10))
        text_y += 60

    # 制限時間の表示
    time_text = font_to_use.render("3. 制限時間: 60秒", True, WHITE)
    screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, text_y))

    # スタートメッセージ
    start_text = pygame.font.SysFont("meiryo", 30, bold=True).render(
        "Enterキーで開始", True, RED
    )
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, text_y + 80))

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
    global score,santa_is_throwing, santa_rotation_angle, throw_start_time
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

            # キー入力処理
            if event.type == pygame.KEYDOWN:
                # アイテムを生成する位置を計算
                item_start_x = santa_x + santa_image.get_width() - 20  # サンタ画像の右端付近
                item_start_y = santa_y + santa_image.get_height() // 2 - 10  # サンタ画像の中央付近

                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    # サンタが投げる動作
                    santa_is_throwing = True
                    santa_rotation_angle = -20  # サンタを少し左に傾ける
                    throw_start_time = pygame.time.get_ticks()  # 投げ動作の開始時間

                    # 投げるアイテムを生成
                    # キー入力処理の変更
                    if event.key == pygame.K_1:
                        items.append(Item(item_start_x, item_start_y, game_image, "game"))
                    elif event.key == pygame.K_2:
                        items.append(Item(item_start_x, item_start_y, clothes_image, "clothes"))
                    elif event.key == pygame.K_3:
                        items.append(Item(item_start_x, item_start_y, comic_image, "comic"))

                    # 効果音を再生
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

        if santa_is_throwing:
            rotated_santa_image = pygame.transform.rotate(santa_image, santa_rotation_angle)
            rotated_rect = rotated_santa_image.get_rect(center=(santa_x + santa_image.get_width() // 2, santa_y + santa_image.get_height() // 2))
            screen.blit(rotated_santa_image, rotated_rect.topleft)

            if pygame.time.get_ticks() - throw_start_time > 300:
                santa_is_throwing = False
                santa_rotation_angle = 0
        else:
            screen.blit(santa_image, (santa_x, santa_y))


        time_text = font.render(f"[Time]: {remaining_time}", True, WHITE)
        score_text = font.render(f"[Score]: {score}", True, WHITE)
        screen.blit(time_text, (10, 10))
        screen.blit(score_text, (180, 10))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    game_over_screen()

def game_over_screen():
    global score

    # スコアをランキングに記録
    save_scores(score)

    # 背景画像を描画
    bg_width, bg_height = start_background_image.get_size()
    bg_x = (screen_width - bg_width) // 2
    bg_y = (screen_height - bg_height) // 2
    screen.blit(start_background_image, (bg_x, bg_y))

    # ゲームオーバー画面の説明文
    instructions = [
        "ゲーム終了！",
        f"最終スコア: {score}",
        "もう一度プレイするにはRキーを押してください",
    ]

    # 説明文の描画位置を計算
    text_y = screen_height // 2 - 60  # 中央付近に配置
    for line in instructions:
        text_color = RED if line.startswith("ゲーム終了") or line.startswith("最終スコア") else WHITE
        text = font.render(line, True, text_color)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, text_y))
        text_y += 40  # 行間を調整

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
                if event.key == pygame.K_r:
                    waiting = False
                    start_screen()  # スタート画面に戻る


# 実行
start_screen()
main_game()
pygame.quit()