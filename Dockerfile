FROM alpine

RUN apk update && \
	apk add oath-toolkit-oathtool

WORKDIR /app

CMD [ "/bin/ash" ]