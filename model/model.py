# file: model.py
from config.constans import *
import pygame
from pathlib import Path
from typing import Optional, Dict

# --- cấu hình ảnh ---
_ASSET_FILES = {
    'start': 'character-bg.png',
    'end': 'home.png',
    'wall': 'wall.png'
}

# cache raw images (pygame.Surface) hoặc None nếu load thất bại
_raw_images: Dict[str, Optional[pygame.Surface]] = {
    'start': None,
    'end': None,
    'wall': None
}

# cache scaled images theo kích thước: _scaled_cache[name][size] = surface
_scaled_cache: Dict[str, Dict[int, pygame.Surface]] = {
    'start': {},
    'end': {},
    'wall': {}
}

def _assets_dir() -> Path:
    """
    Trả về thư mục chứa assets, giả sử cấu trúc:
      project/
        assets/
        model/
          model.py  <-- file này
    Vì vậy assets nằm ở parent của model.
    """
    return Path(__file__).parent.parent / 'assets'

def _load_raw_image(name: str) -> Optional[pygame.Surface]:
    """Load image raw lần đầu (convert_alpha nếu có). Trả về None nếu lỗi."""
    if _raw_images.get(name) is not None:
        return _raw_images[name]

    filename = _ASSET_FILES.get(name)
    if not filename:
        _raw_images[name] = None
        return None

    path = _assets_dir() / filename
    try:
        surf = pygame.image.load(str(path))
        # convert_alpha để giữ transparency nếu ảnh có
        try:
            surf = surf.convert_alpha()
        except Exception:
            surf = surf.convert()
        _raw_images[name] = surf
        return surf
    except Exception:
        # nếu không tìm thấy hoặc lỗi load thì đặt None và tiếp tục dùng màu
        _raw_images[name] = None
        return None

def _get_scaled_image(name: str, size: int) -> Optional[pygame.Surface]:
    """Trả về surface đã scale theo size. Nếu ảnh gốc không có thì trả về None."""
    if name not in _scaled_cache:
        return None
    if size in _scaled_cache[name]:
        return _scaled_cache[name][size]
    raw = _load_raw_image(name)
    if raw is None:
        return None
    try:
        scaled = pygame.transform.smoothscale(raw, (size, size))
    except Exception:
        # fallback to simple scale
        scaled = pygame.transform.scale(raw, (size, size))
    _scaled_cache[name][size] = scaled
    return scaled

# ---------- Class Node ----------
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # chuẩn hoá: x = col * width (ngang), y = row * width (dọc)
        self.x = col * width
        self.y = row * width
        # mặc định dùng màu trắng (các hằng màu lấy từ config.constans)
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    # trạng thái kiểm tra
    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == GREEN

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = BLUE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = ORANGE

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = GREEN

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        """
        Vẽ node:
         - Nếu node là start/end/wall và ảnh tương ứng tồn tại -> blit ảnh scaled
         - Ngược lại -> vẽ rect với màu hiện tại (self.color)
         - Nếu node là path (PURPLE) -> vẽ rect màu PURPLE
        """
        # ưu tiên ảnh cho start
        if self.is_start():
            surf = _get_scaled_image('start', self.width)
            if surf:
                win.blit(surf, (self.x, self.y))
                return
            # fallback: vẽ màu
            pygame.draw.rect(win, BLUE, (self.x, self.y, self.width, self.width))
            return

        if self.is_end():
            surf = _get_scaled_image('end', self.width)
            if surf:
                win.blit(surf, (self.x, self.y))
                return
            pygame.draw.rect(win, GREEN, (self.x, self.y, self.width, self.width))
            return

        if self.is_wall():
            surf = _get_scaled_image('wall', self.width)
            if surf:
                win.blit(surf, (self.x, self.y))
                return
            pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.width))
            return

        # path
        if self.color == PURPLE:
            pygame.draw.rect(win, PURPLE, (self.x, self.y, self.width, self.width))
            return

        # default: ô trống (màu self.color)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])
        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

# --- utility export (nếu cần) ---
def scale_img(img: pygame.Surface, size: int) -> pygame.Surface:
    """Hàm tiện dụng nếu bạn muốn scale thủ công bên ngoài."""
    try:
        return pygame.transform.smoothscale(img, (size, size))
    except Exception:
        return pygame.transform.scale(img, (size, size))
