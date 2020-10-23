import { VaultAccess } from 'node-vault-user-pass';
import * as config from '../config';

// const Vault = new VaultAccess({
//    Authority: ['create', 'read', 'update', 'delete', 'list', 'sudo'],
//    Path: 'path',
//    Policy: 'auth_policy',
//    EndPoint: config.VAULT.url,
//    UserName: 'username',
//    SecretMountPoint: 'secret_zone',
//    Token: config.VAULT.token,
//    CertificateMountPoint: 'certificate'
// });

// export const setup = Vault.Setup();

export const vault = () => {
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
   Vault.Setup();
   return Vault;
};

export const signUp = async (Vault: any, password: string, username: string) => {
   return await Vault.SignUp(password, username);
};

export const login = async (Vault: any, password: string, username: string) => {
   return await Vault.SignIn(password, username);
};

export const write = async (Vault: any, key: string, value: string) => {
   return await Vault.Write(key, value);
};

export const read = async (Vault: any, key: string) => {
   return await Vault.Read(key);
};

export const getUsers = async (Vault: any) => {
   return await Vault.UsersGet();
};
