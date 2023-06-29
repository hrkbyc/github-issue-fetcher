# GitHub Issue Fetcher
このプロジェクトは指定したGitHubのリポジトリからクローズされたイシューの一覧を取得し、それらをCSVファイルに保存します。

## 使い方

1. 最初に、このリポジトリをクローンします:

    ```
    git clone <this_repository>
    ```

2. 次に、必要なパッケージをインストールします:

    ```
    pip install -r requirements.txt
    ```

3. `.env.example` ファイルをコピーして `.env` ファイルを作成します:

    ```
    cp .env.example .env
    ```

    `.env` ファイルを開き、以下の形式で必要な情報を提供します:

    ```
    ACCESS_TOKEN=<your_github_token>
    REPOSITORIES=<your_repositories>
    GITHUB_USER=<your_github_username>
    ```

    ここで、`<your_github_token>` はあなたのGitHubのトークン、 `<your_repositories>` は取得したいイシューのあるリポジトリのリスト（カンマで区切り）、 `<your_github_username>` はあなたのGitHubのユーザー名です。


4. スクリプトを実行します:

    ```
    python fetch_issues.py
    ```

    このスクリプトは、各リポジトリからクローズされたイシューの一覧を取得し、それらを `issues.csv` という名前のCSVファイルに保存します。 各行は、リポジトリ名、イシュー番号、タイトル、クローズされた日付、ラベル、アサインされたユーザー名の一覧です。
