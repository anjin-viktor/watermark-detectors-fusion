import os
import shutil

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tests import filter

def filter_watermark(embedding_level, input_filename, filter_name, filter_params):
    name_prefix = "correlation_tests/" + "/" + str(embedding_level)

    os.makedirs("correlation_tests", exist_ok=True)
    os.makedirs(name_prefix, exist_ok=True)
    os.makedirs(name_prefix + "/" + filter_name, exist_ok=True)
    os.makedirs(name_prefix + "/wo_embedding_" + filter_name, exist_ok=True)

    filename = Path(input_filename)
    filename_wo_ext = filename.with_suffix('')

    watermarked_name = name_prefix + "/watermarked/" + str(filename_wo_ext) + ".bmp"
    filtered_name = name_prefix + "/" + filter_name + "/" + str(filename_wo_ext) + ".bmp"

    filter.run(filter_params, watermarked_name, filtered_name)


def filter_watermarks_multithread(embedding_level, filter_name, filter_params):
    max_threads = os.cpu_count();
    if max_threads > 4:
        max_threads -= 4
    threadPool = ThreadPoolExecutor(max_workers=max_threads)

    directory = os.fsencode("images/")

    futures = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        future = threadPool.submit(filter_watermark, embedding_level, filename, filter_name, filter_params)
        futures.append(future)

    for future in futures:
        future.result()

def filter_watermarks(embedding_level, filter_name, filter_params):
    filter_watermarks_multithread(embedding_level, filter_name, filter_params)

def remove_files(embedding_level, filter_name):
    dir_name = "correlation_tests/" + "/" + str(embedding_level) + "/" + filter_name
    shutil.rmtree(dir_name)

    dir_name = "correlation_tests/" + "/" + str(embedding_level) + "/wo_embedding_" + filter_name
    shutil.rmtree(dir_name)

if __name__ == "__main__":
    embedding_level = 3
    filter_watermarks(embedding_level, "blur", "unsharp=3:3:-0.25:3:3:-0.25")
#    remove_files(dct_watermark, "dct_watermark", embedding_level, "blur")
