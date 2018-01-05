NAME = apca/openldap
VERSION = 1.1.10
LDAP_OPENLDAP_UID=1001
LDAP_OPENLDAP_GID=1002

.PHONY: build build-nocache test tag-latest push push-latest release git-tag-version

build:
	docker build -t $(NAME):$(VERSION) --network host --rm image --build-arg LDAP_OPENLDAP_GID=${LDAP_OPENLDAP_GID} --build-arg LDAP_OPENLDAP_UID=${LDAP_OPENLDAP_UID}

build-nocache:
	docker build -t $(NAME):$(VERSION) --no-cache --rm image --build-arg LDAP_OPENLDAP_GID=${LDAP_OPENLDAP_GID} --build-arg LDAP_OPENLDAP_UID=${LDAP_OPENLDAP_UID}

test:
	env NAME=$(NAME) VERSION=$(VERSION) bats test/test.bats

tag-latest:
	docker tag $(NAME):$(VERSION) $(NAME):latest

push:
	docker push $(NAME):$(VERSION)

push-latest:
	docker push $(NAME):latest

release: build test tag-latest push push-latest

git-tag-version: release
	git tag -a v$(VERSION) -m "v$(VERSION)"
	git push origin v$(VERSION)
