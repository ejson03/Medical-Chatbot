import { VaultAccess } from 'node-vault-user-pass';
import * as config from '../config';

const Vault = new VaultAccess({
   Authority: ['create', 'read', 'update', 'delete', 'list', 'sudo'],
   Path: 'path',
   Policy: 'auth_policy',
   EndPoint: config.VAULT.url,
   UserName: 'username',
   SecretMountPoint: 'secret_zone',
   Token: config.VAULT.token,
   CertificateMountPoint: 'certificate'
});

export const setup = Vault.Setup();

export const signUp = async (password: string, username: string) => {
   return await Vault.SignUp(password, username);
};

export const login = async (password: string, username: string) => {
   return await Vault.SignIn(password, username);
};

export const write = async (key: string, value: string) => {
   return await Vault.Write(key, value);
};

export const read = async (key: string) => {
   return await Vault.Read(key);
};

export const getUsers = async () => {
   return await Vault.UsersGet();
};

export const lookup = async () => {
   return await Vault.TokenLookupSelf();
};
