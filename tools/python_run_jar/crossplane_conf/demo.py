import crossplane

if __name__ == '__main__':
    conf = r'./nginx-bak.conf'
    payload = crossplane.parse(conf, combine=True)
    print(payload)
