import noise
import random
import math

def generate_svg_ripples(
    filename="ripples_vector.svg",
    width=1400,
    height=1400,
    
    # Visual Styling
    background_color="#e6e6e6", # Light grey like the reference
    line_color="#C9C9C9",       # Black lines
    line_width=0.8,
    line_opacity=0.8,
    
    # Density
    num_lines=300,    # Number of vertical lines
    steps_per_line=400, # Resolution of each line (higher = smoother curves)
    
    # Noise / Physics Parameters
    scale=0.003,       # Zoom level of the noise
    distortion=800,    # How much the lines wave left/right
    
    # Domain Warping (The "folding" effect)
    warp_scale=0.009,
    warp_strength=600
):
    print(f"Generating SVG art: {filename}...")
    
    # 1. Setup SVG Header
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    
    # 2. Add Background
    # svg_lines.append(f'<rect width="100%" height="100%" fill="{background_color}" />')

    # Random seeds for the noise layers
    seed_x = random.random() * 1000
    seed_y = random.random() * 1000
    seed_warp = random.random() * 1000

    # 3. Generate Lines
    # We calculate the x-positions across the screen with a small margin
    margin = width * 0.05
    x_step = (width - (margin * 2)) / (num_lines - 1)

    for i in range(num_lines):
        base_x = margin + i * x_step
        path_data = [] # List to hold "command x,y" strings
        
        # Iterate down the Y axis
        for j in range(steps_per_line):
            y = (j / (steps_per_line - 1)) * height
            
            # --- Domain Warping Logic ---
            # We warp the coordinate space before sampling the main noise.
            # This creates the "pinched" or folded look.
            
            # Warp X coordinate
            dx = noise.pnoise2(
                base_x * warp_scale + seed_warp, 
                y * warp_scale, 
                octaves=2
            ) * warp_strength
            
            # Warp Y coordinate (creates vertical compression/extension)
            dy = noise.pnoise2(
                base_x * warp_scale + seed_warp + 100, 
                y * warp_scale, 
                octaves=2
            ) * warp_strength

            warped_x = base_x + dx
            warped_y = y + dy

            # --- Main Displacement ---
            # Now sample the noise using the warped coordinates
            noise_val = noise.pnoise2(
                warped_x * scale + seed_x,
                warped_y * scale + seed_y,
                octaves=4,
                persistence=0.5,
                lacunarity=2.0
            )

            # Calculate final pixel position
            final_x = base_x + (noise_val * distortion)
            final_y = y # We keep Y mostly constant for the vertical flow effect
            
            # Construct SVG Path Command
            # M = Move to (start), L = Line to
            if j == 0:
                path_data.append(f"M {final_x:.2f} {final_y:.2f}")
            else:
                path_data.append(f"L {final_x:.2f} {final_y:.2f}")

        # Combine all points into a single <path> element
        full_path_str = " ".join(path_data)
        
        svg_line = (
            f'<path d="{full_path_str}" '
            f'stroke="{line_color}" '
            f'stroke-width="{line_width}" '
            f'fill="none" '
            f'opacity="{line_opacity}" />'
        )
        svg_lines.append(svg_line)

        # Progress tracker
        if i % 20 == 0:
            print(f"Processed line {i}/{num_lines}")

    # 4. Close SVG tag
    svg_lines.append('</svg>')

    # 5. Write to file
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    
    print("Done! You can open the SVG in any browser or vector editor (Illustrator, Inkscape).")

if __name__ == "__main__":
    generate_svg_ripples(
        filename="wavy_art_output.svg",
        num_lines=200,     # Adjust for density
        distortion=150,    # Adjust for wave width
        warp_strength=100  # Adjust for "knot" intensity
    )