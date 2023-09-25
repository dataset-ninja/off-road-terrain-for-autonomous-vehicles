import supervisely as sly
import os
import csv
from collections import defaultdict
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_name_with_ext
import shutil

from tqdm import tqdm

def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###

    images_path = os.path.join("Off-Road Terrain Dataset for Autonomous Vehicles","Images","Images")
    sensors_path = os.path.join("Off-Road Terrain Dataset for Autonomous Vehicles","SensorData")
    # masks_path = "/home/alex/DATASETS/TODO/Off-Road Terrain Attention/archive/AttentionRegion/AttentionRegion/light"
    tsm1_labels_path = os.path.join("Off-Road Terrain Dataset for Autonomous Vehicles","ImageLabels","tsm_1_labels.csv")
    tsm2_labels_path = os.path.join("Off-Road Terrain Dataset for Autonomous Vehicles","ImageLabels","tsm_2_labels.csv")
    ds_name = "ds"
    batch_size = 50
    masks_ext = ".png"

    proj_dict = defaultdict()
    possible_tags = []

    for seq in os.listdir(sensors_path):
        img_seq = seq[:10]
        accelerometer = {}
        gps = {}
        gyroscope = {}
        magnetometer = {}
        record = {}
        file_name_to_dict = {
            "accelerometer_calibrated_split.csv": accelerometer,
            "gps.csv": gps,
            "gyroscope_calibrated_split.csv": gyroscope,
            "magnetometer_split.csv": magnetometer,
            "record.csv": record,
        }
        file_name_to_dict = {
        "accelerometer_calibrated_split.csv": accelerometer,
        "gps.csv": gps,
        "gyroscope_calibrated_split.csv": gyroscope,
        "magnetometer_split.csv": magnetometer,
        "record.csv": record,
        }

        curr_sensors_path = os.path.join(sensors_path, seq)
        for sensor_name in list(file_name_to_dict.keys()):
            file_path = os.path.join(curr_sensors_path, sensor_name)
            with open(file_path, "r") as file:
                csvreader = csv.reader(file)
                for idx, row in enumerate(csvreader):
                    if idx != 0:
                        file_name_to_dict[sensor_name]["{}s{}ms".format(row[1], str(int(float((row[2])))))] = {name:[row[i+3]] for i, name in enumerate(dict_names[3:])}
                    else: 
                        dict_names = [name for name in row]
                        possible_tags.extend(dict_names)
        proj_dict[img_seq] = file_name_to_dict
    

    def create_ann(image_path):
        labels = []
        tags = []
        img_height = 2160
        img_wight = 3840

        head,filename = os.path.split(image_path)
        filename = filename[:-4]

        tag_s = sly.Tag(tag_seq, value=os.path.basename(head))
        tags.append(tag_s)

        tsm1_data = name_to_tsm1.get(get_file_name_with_ext(image_path))
        if tsm1_data is not None:
            for cat in tsm1_data:
                tag_name = cat
                tag_value = str(tsm1_data[cat])
                tag = [sly.Tag(tagmeta, value=tag_value) for tagmeta in tag_metas if tagmeta.name == tag_name]
                tags.extend(tag)
        tsm2_data = name_to_tsm2.get(get_file_name_with_ext(image_path))
        if tsm2_data is not None:
            for cat in tsm2_data:
                tag_name = cat
                tag_value = str(tsm2_data[cat])
                tag = [sly.Tag(tagmeta, value=tag_value) for tagmeta in tag_metas if tagmeta.name == tag_name]
                tags.extend(tag)

        timestamp_and_timestamp_ms = False

        for csvfile in proj_dict[os.path.basename(head)]:
            try:
                for cat in proj_dict[os.path.basename(head)][csvfile][filename]:
                    if cat:
                        if timestamp_and_timestamp_ms and "timestamp" in cat:
                            continue
                        if "timestamp_ms" in cat and not timestamp_and_timestamp_ms:
                            timestamp_and_timestamp_ms = True
                        tag_value = proj_dict[os.path.basename(head)][csvfile][filename][cat]
                        if isinstance(tag_value,list):
                            tag_value = str(tag_value[0])
                        else: 
                            tag_value = str(tag_value)
                        tag_name = cat
                        tag = [sly.Tag(tagmeta, value=tag_value) for tagmeta in tag_metas if tagmeta.name == tag_name]
                        tags.extend(tag)
            except KeyError:
                pass

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)


    possible_tags.extend(["tsm1_original","tsm1_k2","tsm1_k3","tsm1_k4","tsm2_original","tsm2_k2","tsm2_k3","tsm2_k4"])
    possible_tags = set(possible_tags)
    tag_metas = [sly.TagMeta(name, sly.TagValueType.ANY_STRING) for name in possible_tags if name and "utc_" not in name]
    tag_seq = sly.TagMeta("sequence", sly.TagValueType.ANY_STRING)
    tag_metas.extend([tag_seq])
    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        tag_metas=tag_metas,
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    name_to_tsm1 = {}
    with open(tsm1_labels_path, "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            if idx != 0:
                name_to_tsm1[row[0]] = {"tsm1_original": row[1], "tsm1_k2": row[2], "tsm1_k3": row[3], "tsm1_k4": row[4]}

    name_to_tsm2 = {}
    with open(tsm2_labels_path, "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            if idx != 0:
                name_to_tsm2[row[0]] = {"tsm2_original": row[1], "tsm2_k2": row[2], "tsm2_k3": row[3], "tsm2_k4": row[4]}

    for subfolder in os.listdir(images_path):
        curr_images_path = os.path.join(images_path, subfolder)
        accelerometer = {}
        gps = {}
        gyroscope = {}
        magnetometer = {}
        record = {}
        
        images_names = os.listdir(curr_images_path)

        progress = sly.Progress(
            "Create dataset {}, add {} data".format(ds_name, subfolder), len(images_names)
        )

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            images_pathes_batch = [
                os.path.join(curr_images_path, image_path) for image_path in img_names_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns_batch = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns_batch)

            progress.iters_done_report(len(img_names_batch))
    
    return project



