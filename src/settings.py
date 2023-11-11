from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "Off-Road Terrain for Autonomous Vehicles"
PROJECT_NAME_FULL: str = "Off-Road Terrain for Autonomous Vehicles"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Unknown()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Automotive(is_used=True)]
CATEGORY: Category = Category.SelfDriving()

CV_TASKS: List[CVTask] = [CVTask.Identification()]
ANNOTATION_TYPES: List[AnnotationType] = []

RELEASE_DATE: Optional[str] = None  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = 2021

HOMEPAGE_URL: str = "https://www.kaggle.com/datasets/magnumresearchgroup/offroad-terrain-dataset-for-autonomous-vehicles"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 4944149
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/off-road-terrain-for-autonomous-vehicles"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = ["https://www.kaggle.com/datasets/magnumresearchgroup/offroad-terrain-dataset-for-autonomous-vehicles"]
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = None
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = ["https://www.dre.vanderbilt.edu/~schmidt/PDF/paper_1.pdf"]
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = {"GitHub": "https://github.com/magnumresearchgroup/TerrainRoughnessPrediction"}

CITATION_URL: Optional[str] = "https://www.kaggle.com/datasets/magnumresearchgroup/offroad-terrain-dataset-for-autonomous-vehicles"
AUTHORS: Optional[List[str]] = ["Gabriela Gresenz", "Jules White", "Douglas C. Schmidt"]
AUTHORS_CONTACTS: Optional[List[str]] = ["gabriela.r.gresenz@vanderbilt.edu", "jules.white@vanderbilt.edu", "douglas.c.schmidt@vanderbilt.edu"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = ["Vanderbilt University"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = ["https://www.vanderbilt.edu/"]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {"__POSTTEXT__": "Dataset contains the corresponding sensor data from a global positioning system (GPS, inertial measurement units (IMUs), a wheel rotation speed sensor, z-axis acceleration). In general, all sensor and label data recorded in seven CSV files (<i>accelerometer_calibrated_split.csv</i>, <i>gps.csv</i>, <i>gyroscope_calibrated_split.csv</i>, <i>magnetometer_split.csv</i> and <i>record.csv</i> - for Sensor Data, <i>tsm_1_labels.csv</i>, </i>tsm_2_labels.csv</i> - for Image Labels). All data has been carefully transferred to tag format: ***tsm1_original***, ***tsm2_k2*** ... etc. from <i>tsm_1_labels.csv</i> and tsm_2_labels, ***accel_x (counts)***, ***calibrated_accel_x (g)***... etc. from <i>accelerometer_calibrated_split.csv</i> etc. Each column in the source data corresponds to a tag, except utc_s(s) and utc_ms(ms) (this data contains in image name). Please note, that not every image has a tag due to differences in the frequency of data collection."}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
