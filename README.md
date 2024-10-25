# aws-cdk

AWS CDK（AWS リソースを宣言的にデプロイするIaCツール）のサンプルをまとめたものです。

|サンプル|内容|補足|
|:--|:--|:--|
|project_s3|SSE-KMS暗号化タイプを設定したS3バケット||

## 環境構築

### 前提

- Windows11
- AWSへインターネットアクセスしているオンプレ端末

### AWS CLI インストール

以下の公式手順に従ってインストール。

[https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/getting-started-install.html)

### CLIユーザの作成と認証設定

以下の公式ドキュメントを参考に、スイッチロール以外の権限を持たないCLIアクセス用のユーザを作成し、そこから必要な権限を持つロールにスイッチロールして操作するようにします。

[https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html)

#### IAMユーザ作成

仮にメインアカウント名が`XXXXX`なので、`XXXXX-cli`という名前のIAMユーザを作成します。マネジメントコンソールへのアクセスは不要のため、「AWSマネジメントコンソールへのユーザアクセスを提供する」はオフ。また、IAMポリシ－はこの時点では設定せず、後から追加します。

アカウントを作成したら、MFAの設定とアクセスキーの払い出しを行っておきます。

#### IAKロール作成

次に、`XXXXX-cli`ユーザがスイッチする`CLIUserRole`ロールを作成します。ポリシーは操作に必要な権限を与えますが、ここではAWS管理ポリシーの`AdministratorAccess`ポリシーを与えます。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        }
    ]
}
```

信頼されたエンティティは先ほど作成した`XXXXX-cli`とし、MFAが有効の場合のみスイッチロールできるようにします。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<account_id>:user/XXXXX-cli"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "Bool": {
                    "aws:MultiFactorAuthPresent": "true"
                }
            }
        }
    ]
}
```

#### IAMポリシー

最後に、以下の`CLIUserAssumeRolePolicy`ポリシーを作成し、`XXXXX-cli`ユーザにアタッチすることで、ユーザが`CLIUserRole`へスイッチロールできるように設定します。

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AssumeRole",
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Resource": [
                "arn:aws:iam::<account_id>:role/CLIUserRole"
            ]
        }
    ]
}
```

#### CLI設定

ここまで設定したら、後はCLI側の設定を行います。`XXXXX-cli`のアクセスキーとシークレットアクセスキーを使って初期設定を行います。

```
> aws configure
AWS Access Key ID [****************]: 
AWS Secret Access Key [****************]: 
Default region name [ap-northeast-1]: 
Default output format [json]: 
```

`C:\User\<user_name>\.aws/config`というファイルが作成されるため、ロールを設定するための設定を追記します。

```ini
[default]
region = ap-northeast-1
output = json
role_arn = arn:aws:iam::<account_id>:role/CLIUserRole
source_profile = default
mfa_serial = arn:aws:iam::<account_id>:mfa/XXXXX-cli
```

### 接続確認

適当なコマンドを実行すると、MFAの入力が求められるので、認証することで実行できるようになります。一定時間経過するまでは、一度認証すればしばらくの間MFAの入力は不要です。

```
$ aws s3 ls
Enter MFA code for arn:aws:iam::<account_id>:mfa/XXXXX-cli:
2024-10-25 10:09:33 XXXXXX
```

### AWS CDK インストール

Node.jsが必要なので、インストールしたうえで`aws-cdk`をインストールします。

[https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/getting_started.html](https://docs.aws.amazon.com/ja_jp/cdk/v2/guide/getting_started.html)

```bash
# AWS CDK CLIのインストール
npm install -g aws-cdk
```

### 環境変数

```bash
set CDK_DEFAULT_ACCOUNT=<account_id>
set CDK_DEFAULT_REGION=ap-northeast-1
```

## 実行方法

### プロジェクト作成

```bash
md project-XX
cd project-XX
cdk init app --language python
.\source.bat
pip install --upgrade -r requirements.txt
```

### 操作

```bash
# 作成
cdk deploy

# 削除
cdk destroy

# 確認
cdk ls
```

## References

- [https://docs.aws.amazon.com/cdk/api/v2/python/](https://docs.aws.amazon.com/cdk/api/v2/python/)
