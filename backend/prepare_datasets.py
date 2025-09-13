# import os
# import shutil
# import pandas as pd
# from sklearn.model_selection import train_test_split

# # ⚠️ Update this path to where you extracted HAM10000
# DATASET_DIR = "./HAM10000"  # Use relative path
# IMAGES_DIR = os.path.join(DATASET_DIR, "images")  # folder with all .jpg files
# METADATA_FILE = os.path.join(DATASET_DIR, "HAM10000_metadata.csv")

# OUTPUT_DIR = "dataset"  # where train/ and val/ will be created
# VAL_SPLIT = 0.2  # 20% for validation

# # Load metadata
# df = pd.read_csv(METADATA_FILE)

# # Get image path and class (dx column = diagnosis label)
# df['path'] = df['image_id'].map(lambda x: os.path.join(IMAGES_DIR, f"{x}.jpg"))
# df = df[['path', 'dx']]  # keep only path and label

# # Train-validation split
# train_df, val_df = train_test_split(df, test_size=VAL_SPLIT, stratify=df['dx'], random_state=42)

# def make_dirs(base, classes):
#     for cls in classes:
#         os.makedirs(os.path.join(base, cls), exist_ok=True)

# # Create folders
# classes = df['dx'].unique()
# make_dirs(os.path.join(OUTPUT_DIR, "train"), classes)
# make_dirs(os.path.join(OUTPUT_DIR, "val"), classes)

# # Function to copy images
# def copy_images(dataframe, split):
#     for _, row in dataframe.iterrows():
#         src = row['path']
#         dst = os.path.join(OUTPUT_DIR, split, row['dx'], os.path.basename(src))
#         shutil.copy(src, dst)

# print("Copying training images...")
# copy_images(train_df, "train")

# print("Copying validation images...")
# copy_images(val_df, "val")

# print("✅ Dataset prepared! Check the 'dataset/' folder:")
# print(os.listdir(OUTPUT_DIR))
import os
import shutil
import pandas as pd
from sklearn.model_selection import train_test_split

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_DIR = os.path.join(BASE_DIR, "images")  
META_CSV = os.path.join(BASE_DIR,"HAM10000_metadata.csv")  
OUTPUT_DIR = os.path.join(BASE_DIR, "dataset")

# Make sure output dirs exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load metadata
print("📂 Loading metadata...")
df = pd.read_csv(META_CSV)

# Look at available images in the folder
available_images = os.listdir(IMAGE_DIR)
available_images_lower = {img.lower() for img in available_images}
print(f"✅ Found {len(available_images)} images available in 'images/'")

# Match metadata to actual files (case-insensitive)
def find_file(image_id):
    candidates = [f"{image_id}.jpg", f"{image_id}.jpeg", f"{image_id}.png"]
    for c in candidates:
        if c.lower() in available_images_lower:
            return c
    return None

df["image_file"] = df["image_id"].apply(find_file)
df = df.dropna(subset=["image_file"])  # keep only rows with matching images

print(f"✅ After filtering, {len(df)} images remain.")

# Split into train/val
train_df, val_df = train_test_split(
    df, test_size=0.2, stratify=df['dx'], random_state=42
)

def copy_images(subset_df, subset_name):
    print(f"📦 Copying {subset_name} images...")
    for _, row in subset_df.iterrows():
        label = row['dx']
        src = os.path.join(IMAGE_DIR, row['image_file'])
        dst_dir = os.path.join(OUTPUT_DIR, subset_name, label)
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, row['image_file'])
        try:
            shutil.copy(src, dst)
        except Exception as e:
            print(f"⚠️ Skipped {src}: {e}")

# Copy train and val images
copy_images(train_df, "train")
copy_images(val_df, "val")

print("🎉 Dataset prepared successfully!")
