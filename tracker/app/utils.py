from array import array


def string_to_bytes(string):
    array_key = array('b')
    array_key.frombytes(string.encode())
    return array_key.tobytes()


def get_client_id(request):
    return request.remote_ip
