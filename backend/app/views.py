from rest_framework import viewsets
from .models import Beat, Rap
from .serializers import BeatSerializer, RapSerializer

"""import matlab.engine
eng = matlab.engine.start_matlab()
test_array = matlab.double([1, 2, 3])
BPM = eng.outputBPM(test_array)
print(BPM)"""


class BeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Beat.objects.all()
    serializer_class = BeatSerializer


class RapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rap.objects.all()
    serializer_class = RapSerializer
