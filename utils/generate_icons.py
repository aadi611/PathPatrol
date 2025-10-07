"""
Generate PWA icons for PathPatrol
This script creates all required icon sizes for the Progressive Web App
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def create_icon(size, output_path):
    """
    Create a PathPatrol icon
    
    Args:
        size: Icon size (width and height)
        output_path: Path to save the icon
    """
    # Create image with gradient background
    img = Image.new('RGB', (size, size), color='#0f3460')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient effect (simulate with rectangles)
    for i in range(size):
        # Calculate gradient color
        r = int(26 + (15 - 26) * (i / size))
        g = int(26 + (52 - 26) * (i / size))
        b = int(46 + (96 - 46) * (i / size))
        color = (r, g, b)
        draw.rectangle([(0, i), (size, i + 1)], fill=color)
    
    # Draw road icon (simplified)
    road_width = size // 3
    road_x = (size - road_width) // 2
    
    # Road background
    draw.rectangle(
        [(road_x, 0), (road_x + road_width, size)],
        fill='#333333'
    )
    
    # Road markings (dashed lines)
    dash_height = size // 15
    dash_gap = size // 10
    dash_width = road_width // 10
    center_x = size // 2
    
    y = dash_gap
    while y < size:
        draw.rectangle(
            [(center_x - dash_width // 2, y), 
             (center_x + dash_width // 2, y + dash_height)],
            fill='#ffcc00'
        )
        y += dash_height + dash_gap
    
    # Draw pothole symbol (warning triangle or circle)
    pothole_size = size // 4
    pothole_x = size // 2
    pothole_y = size // 2
    
    # Draw red warning circle
    draw.ellipse(
        [(pothole_x - pothole_size // 2, pothole_y - pothole_size // 2),
         (pothole_x + pothole_size // 2, pothole_y + pothole_size // 2)],
        fill='#ff4c4c',
        outline='#ffffff',
        width=max(2, size // 100)
    )
    
    # Draw exclamation mark
    exclamation_height = pothole_size // 2
    exclamation_width = size // 50
    
    # Exclamation line
    draw.rectangle(
        [(pothole_x - exclamation_width, pothole_y - exclamation_height // 2),
         (pothole_x + exclamation_width, pothole_y + exclamation_height // 6)],
        fill='#ffffff'
    )
    
    # Exclamation dot
    dot_size = size // 40
    draw.ellipse(
        [(pothole_x - dot_size, pothole_y + exclamation_height // 4),
         (pothole_x + dot_size, pothole_y + exclamation_height // 2)],
        fill='#ffffff'
    )
    
    # Save the icon
    img.save(output_path, 'PNG', quality=95)
    print(f"Created icon: {output_path}")


def generate_all_icons():
    """Generate all required icon sizes"""
    # Icon sizes required for PWA
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # Create icons directory
    icons_dir = Path(__file__).parent.parent / 'static' / 'icons'
    icons_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating PWA icons...")
    for size in sizes:
        output_path = icons_dir / f'icon-{size}x{size}.png'
        create_icon(size, output_path)
    
    print(f"\n✅ All {len(sizes)} icons generated successfully!")
    print(f"📁 Location: {icons_dir}")
    
    # Create a favicon as well
    favicon_path = icons_dir.parent / 'favicon.ico'
    create_icon(32, icons_dir / 'favicon-32.png')
    
    # Convert to ICO (requires PIL)
    try:
        favicon_img = Image.open(icons_dir / 'favicon-32.png')
        favicon_img.save(favicon_path, format='ICO')
        print(f"Created favicon: {favicon_path}")
    except Exception as e:
        print(f"Note: Could not create favicon.ico: {e}")
        print("You can convert favicon-32.png to .ico using an online tool")


if __name__ == '__main__':
    generate_all_icons()
