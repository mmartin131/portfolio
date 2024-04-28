import os.path
import pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import zipfile
import constants

class LesionData: 
    Data_Dir = constants.DATA_DIR
    _base_url = constants.BASE_URL
    _images_zip_files = [
        "ISIC_2019_Training_Input.zip",
        "ISIC_2019_Test_Input.zip",]
    _metadata_csv_files = [
        "ISIC_2019_Training_Metadata.csv",
        "ISIC_2019_Training_GroundTruth.csv",
        "ISIC_2019_Test_Metadata.csv",]
    _all_files = _images_zip_files + _metadata_csv_files
    

    def __init__(self):
        self.Data_Dir = LesionData.Data_Dir
        self._base_url = LesionData._base_url
        self._images_zip_files = LesionData._images_zip_files
        self._metadata_csv_files = LesionData._metadata_csv_files
        self._all_files = LesionData._all_files
        
        if not os.path.exists(self.Data_Dir + "/"):
            os.mkdir(self.Data_Dir)
        
        pass

    def download(self, force_download:bool=False):
        self._download_concurrent(force_download=force_download, max_workers=20)
        

    def download_and_unzip(self, force:bool=False):
        self.download(force_download=force)
        
        if force:
            self.unzip(max_workers=100)
        
    def _download_concurrent(self, force_download:bool, max_workers:int):
        threads= []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            
            for file_name in self._all_files:
                out_file_path =  self._get_local_path(file_name)
                
                if force_download or (not os.path.exists(out_file_path)):     
                    threads.append(
                        executor.submit(
                            self._download_file,
                            self._base_url + file_name,
                            out_file_path,
                        ))

            for task in as_completed(threads):
                task.result()
    
    def _get_local_path(self, file_name:str):
        return self.Data_Dir + "/" + file_name
    
    def _download_file(self, url, out_file_path):
        try:
            print("Downloading file " + url + " to " + out_file_path)
            response = requests.get(url, stream=True)
            file = open(out_file_path, "wb")
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
            print("Done downloading file " + out_file_path)        
            return response.status_code
        except requests.exceptions.RequestException as e:
            print(e)
            return e
        
        
    def unzip(self, max_workers:int=100):
        threads = []
        with ThreadPoolExecutor(max_workers) as executor:
            for zfname in self._images_zip_files:
                local_file_path =  self._get_local_path(zfname)
                out_file_path = self._get_local_path("")
            
                threads.append(
                        executor.submit(
                            self._unzip_file,
                            local_file_path,
                            out_file_path,
                            max_workers
                        ))
                
            for future in as_completed(threads):
                    try:
                        future.result()
                    except Exception as exc:
                        print("Failed to unzip file " + str(exc))
                
 
    def _unzip_file(self, file, out_file_path, max_workers): 
        print("\nUnzipping " + file)
        threads = []
        with zipfile.ZipFile(file, 'r') as handle:
            with ThreadPoolExecutor(max_workers) as executor:
                future_to_file = {}

                for file_name in handle.namelist():
                    threads.append(executor.submit(handle.extract, file_name, out_file_path))

                for future in as_completed(threads):
                    try:
                        future.result()
                    except Exception as exc:
                        print("Failed to unzip " + str(exc))
                
        print("Done unzipping file " + file)

        