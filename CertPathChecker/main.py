# Desenvolvido pelos alunos do Curso Tecnologo de Seguranca da Informacao - Unisinos
# Denis Steffen, Jean Schmidt, Luis Gustavo Nunes, Rafael Alves
# 2018/2 - Segurança em Comercio Eletronico
# Prof. Me. Luciano Ignaczak 

from pathlib import Path
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA1
import base64
import requests

creditos = 'Desenvolvido pelos alunos do Curso Tecnologo de Seguranca da Informacao - Unisinos \n' \
         + 'Denis Steffen, Jean Schmidt, Luis Gustavo Nunes, Rafael Alves \n' \
         + '2018/2 - Segurança em Comercio Eletronico \n' \
         + 'Prof. Me. Luciano Ignaczak \n'

def searchCert(pathCert, tipo):
    if pathCert.exists():
        if pathCert.suffix == '.cer' \
        or pathCert.suffix == '.crt':
            pass
        else:
            print(tipo + ': Tipo de arquivo do certificado deve ser .cer ou .crt')
            return False
    else:
        print(tipo + ': Arquivo certificado nao encontrado, favor verificar!')
        return False

    return True

def loadCertFromPath(pathCert, tipo):
    return loadCert(pathCert.read_bytes(), tipo)

def loadCert(binCert, tipo):
    try:
        cert = x509.load_der_x509_certificate(binCert, default_backend())
    except:
        try:
            cert = x509.load_pem_x509_certificate(binCert, default_backend())
        except:
            print(tipo + ': Tipo de arquivo invalido, favor verificar')
            return
    
    return cert

def getSubjectKeyIdentifier(Cert):
    if Cert is None:
        print('Erro em getSubjectKeyIdentifier')
        return

    keyId = ''
    keyId = Cert.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value.digest

    return keyId

def getAuthorityKeyIdentifier(Cert):
    keyId = ''
    keyId = Cert.extensions.get_extension_for_class(x509.AuthorityKeyIdentifier).value.key_identifier

    return keyId

def getIssuerCert(Cert, subj):
    url = ''
    listAccessInfo = Cert.extensions.get_extension_for_class(x509.AuthorityInformationAccess).value._descriptions
    for i in listAccessInfo:
        if i.access_method == x509.oid.AuthorityInformationAccessOID.CA_ISSUERS:
            url = i.access_location.value

    if url == '':
        if getAuthorityKeyIdentifier(Cert) == '':
            print(subj + ': sem informacao de acesso para o Certificado do Emissor.')
            return
        else:
            return Cert

    r = requests.get(url)
    if r.status_code != 200:
        print(subj + ': Certificado do emissor do certificado de inacessivel.')
        return
    else:
        return loadCert(r.content, 'Emissor de ' + subj)       

def getOCSPStatus(Cert, issuerCert, subj):
    ocspURL = ''

    listAccessInfo = Cert.extensions.get_extension_for_class(x509.AuthorityInformationAccess).value._descriptions

    for i in listAccessInfo:
        if i.access_method == x509.oid.AuthorityInformationAccessOID.OCSP:
            ocspURL = i.access_location.value

    if ocspURL == '':
        print(subj + ': sem informacao de acesso OCSP.')
        return False

    builder = x509.ocsp.OCSPRequestBuilder()
    builder = builder.add_certificate(Cert, issuerCert, SHA1())
    req = builder.build()

    ocspURL += '/' + base64.b64encode(req.public_bytes(serialization.Encoding.DER)).decode("utf-8")

    r = requests.get(ocspURL)
    if r.status_code != 200:
        print(subj + ': servico OCSP esta inacessivel.')
        return False
    else:
        ocsp_resp = x509.ocsp.load_der_ocsp_response(r.content)

        if ocsp_resp == x509.ocsp.OCSPResponseStatus.UNAUTHORIZED:
            return False
        else:
            return True

def validateCert(Cert):
    retorno     = ''
    subj_cn     = Cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[0].value
    issuer_Cert = ''

    print(subj_cn + ": validando...")

    if Cert.not_valid_before > datetime.today():
        print(subj_cn + ': Certificado ainda nao se tornou valido.')
        retorno = False        
        
    if Cert.not_valid_after < datetime.today():
        print(subj_cn + ': Certificado ja expirou.')
        retorno = False

    if retorno == '':
        print(subj_cn + ': certificado dentro do periodo de validade')

        if Cert.issuer == Cert.subject:
            #Certificado root  
            if getSubjectKeyIdentifier(Cert) == getSubjectKeyIdentifier(rootCert):
                print(subj_cn + ': KeyIdentifier confere com SubjectKeyIdentifier do Certificado Root')
                retorno = True
            else:
                print(subj_cn + ': KeyIdentifier nao confere com SubjectKeyIdentifier do Certificado Root')
                retorno = False        
        else:
            #Certificado de entidade final/subdominio
            issuer_Cert = getIssuerCert(Cert, subj_cn)

            if issuer_Cert == Cert:
                #O proximo certificado da cadeia e o Root
                if getAuthorityKeyIdentifier(Cert) == getSubjectKeyIdentifier(rootCert):
                    print(subj_cn + ': AuthorityKeyIdentifier confere com SubjectKeyIdentifier do Certificado Root')
                    
                    if getOCSPStatus(Cert, rootCert, subj_cn) == False:
                        print(subj_cn + ': Certificado esta revogado')
                        retorno = False
                    else:
                        print(subj_cn + ': Certificado valido')
                        retorno = validateCert(rootCert)
                else:
                    print(subj_cn + ': AuthorityKeyIdentifier nao confere com SubjectKeyIdentifier do Certificado Root')
                    retorno = False
            else:
                if getSubjectKeyIdentifier(issuer_Cert) != getAuthorityKeyIdentifier(Cert):
                    print(subj_cn + ': AuthorityKeyIdentifier invalido')
                    retorno = False
                else:
                    if getOCSPStatus(Cert, issuer_Cert, subj_cn) == False:
                        print(subj_cn + ': Certificado esta revogado')
                        retorno = False
                    else:
                        print(subj_cn + ': Certificado valido')
                        retorno = validateCert(issuer_Cert)
    
    return retorno

while True:
    pathRootCert      = ''
    pathEndEntityCert = ''
    endEntityCert     = ''

    print('CertPathChecker v1.0')
    print(creditos)    
    print('Para sair, informe quit!')
    pathRootCert = input('Informe o caminho do certificado Root:')
    
    if pathRootCert == 'quit!':
        break    
    
    pathEndEntityCert = input('Informe o caminho do certificado de Entidade Final:')
    
    if pathEndEntityCert == 'quit!':
        break
    else:
        pathRootCert      = Path(pathRootCert)
        pathEndEntityCert = Path(pathEndEntityCert)

        if  searchCert(pathRootCert, 'Root') \
        and searchCert(pathEndEntityCert, 'Entidade Final'):
            rootCert      = loadCertFromPath(pathRootCert, 'Root')
            endEntityCert = loadCertFromPath(pathEndEntityCert, 'Entidade Final')

            if pathRootCert      is None \
            or pathEndEntityCert is None:
                pass
            else:
                if validateCert(endEntityCert):
                    print("Cadeia de certificados valida!")
                else:
                    print("Cadeia de certificados invalida!")
        else:
            pass

    print('\n\n')