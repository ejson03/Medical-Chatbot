import { VaultAccess } from 'node-vault-user-pass';
import * as config from '../config';

export const Vault = new VaultAccess({
   Authority: ['create', 'read', 'update', 'delete', 'list', 'sudo'],
   Path: 'path',
   Policy: 'auth_policy',
   EndPoint: config.VAULT.url,
   UserName: 'username',
   SecretMountPoint: 'secret_zone',
   Token: config.VAULT.token,
   CertificateMountPoint: 'certificate',
   AltToken: ''
});

Vault.Setup();

export const vaultFromToken = async (token: string) => {
   const clientVault = new VaultAccess({
      Authority: ['create', 'read', 'update', 'delete', 'list'],
      Path: 'path',
      Policy: 'auth_policy',
      EndPoint: config.VAULT.url,
      UserName: 'username',
      SecretMountPoint: 'secret_zone',
      Token: token,
      CertificateMountPoint: 'certificate',
      AltToken: ''
   });
   const username = (await clientVault.TokenLookup(undefined)).data.meta.username;
   clientVault.Config.UserName = username;
   return clientVault;
};

export const signUp = async (vault: VaultAccess, password: string, username: string) => {
   const token = vault.Config.Token;
   const result = await vault.SignUp(password, username);
   vault.Config.Token = token;
   return result;
};

export const login = async (vault: VaultAccess, password: string, username: string) => {
   const token = vault.Config.Token;
   const result = await vault.SignIn(password, username);
   vault.Config.Token = token;
   vault.vault.token = token;
   return result;
};

export const write = async (vault: VaultAccess, key: string, value: string) => {
   return await vault.Write(key, value);
};

export const read = async (vault: VaultAccess, key: string) => {
   return await vault.Read(key);
};

export const getUsers = async (vault: VaultAccess) => {
   return await vault.UsersGet();
};
