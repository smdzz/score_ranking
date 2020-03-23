import json

from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from player_api.models import ClientScore
from score_ranking.settings import redis_client


class ClientScoreViewSet(APIView):

    def post(self, request):
        """客户端上传客户端号和分数(注意：并不会上传排名,客户端无法上传排名),同一个客户端可以多次上传分数，取最新的一次分数"""
        client = request.POST.get("client")
        try:
            score = int(request.POST.get("score"))
            if score < 0 or score > 10000000:
                return Response({'code': 10001, 'data': '参数错误'})
        except:
            return Response({'code': 10001, 'data': '参数错误'})
        if not (client and score):
            return Response({'code': 10002, 'data': '参数缺失'})

        try:
            client_score = ClientScore.objects.get(client=client)
            client_score.score = score
            client_score.save()
        except:
            client_score = ClientScore.objects.create(client=client, score=score)
        redis_client.zadd("client_score", {client: score})
        client_score = json.loads(serializers.serialize('json', [client_score]))[0]["fields"]
        return Response({'code': 10000, 'data': client_score})

    def get(self, request):
        """客户端查询排行榜"""
        client = request.GET.get("client")
        start = int(request.GET.get("start", 1))
        end = int(request.GET.get("end", 10))

        rank_client = redis_client.zrange("client_score", start - 1, end - 1)
        response = []
        for x in rank_client:
            response.append({"rank": start, "client": x.decode("utf-8"),
                             "score": int(redis_client.zscore("client_score", x.decode("utf-8")))})
            start += 1

        response.append({"rank": redis_client.zrank("client_score", client) + 1, "client": client,
                         "score": redis_client.zscore("client_score", client)})
        return Response({'code': 10000, 'data': response})


