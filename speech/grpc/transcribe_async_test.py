# Copyright 2016, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re

from google.cloud import storage

from transcribe_async import main


def test_main(resource, capsys):

    # Upload an audio file to the default testing CLOUD_STORAGE_BUCKET
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(os.environ.get('CLOUD_STORAGE_BUCKET'))
    blob = bucket.blob('audio.raw')
    blob.upload_from_filename('speech/grpc/resources/audio.raw')

    # Run the transcribe_async sample on the audio file, verify correct results
    speech_storage_uri = 'gs://' + os.environ.get('CLOUD_STORAGE_BUCKET')
    speech_storage_uri += '/audio.raw'
    main(speech_storage_uri, 'LINEAR16', 16000)
    out, err = capsys.readouterr()
    assert re.search(r'how old is the Brooklyn Bridge', out, re.DOTALL | re.I)

    # Delete audio file from storage bucket
    blob.delete()
