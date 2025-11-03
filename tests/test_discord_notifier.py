"""
Discord Notifierのユニットテスト

モックを使用した単体テスト（実際のWebhook不要）
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.notifiers.discord_notifier import DiscordNotifier


class TestDiscordNotifierInit:
    """初期化テスト"""
    
    def test_init_success(self):
        """正常な初期化"""
        webhook_url = "https://discord.com/api/webhooks/123/abc"
        notifier = DiscordNotifier(webhook_url)
        assert notifier.webhook_url == webhook_url
    
    def test_init_empty_webhook_url(self):
        """空のWebhook URLでの初期化エラー"""
        with pytest.raises(ValueError, match="Discord Webhook URLが設定されていません"):
            DiscordNotifier("")
    
    def test_init_none_webhook_url(self):
        """NoneのWebhook URLでの初期化エラー"""
        with pytest.raises(ValueError, match="Discord Webhook URLが設定されていません"):
            DiscordNotifier(None)


class TestDiscordNotifierTruncate:
    """テキスト切り詰めテスト"""
    
    def test_truncate_short_text(self):
        """短いテキスト（切り詰め不要）"""
        text = "短いテキスト"
        result = DiscordNotifier._truncate(text, 100)
        assert result == text
    
    def test_truncate_exact_length(self):
        """ちょうど最大長のテキスト"""
        text = "a" * 100
        result = DiscordNotifier._truncate(text, 100)
        assert result == text
    
    def test_truncate_long_text(self):
        """長いテキスト（切り詰めが必要）"""
        text = "a" * 200
        result = DiscordNotifier._truncate(text, 100)
        assert len(result) == 100
        assert result.endswith("...")
        assert result == "a" * 97 + "..."
    
    def test_truncate_empty_text(self):
        """空のテキスト"""
        result = DiscordNotifier._truncate("", 100)
        assert result == ""


class TestDiscordNotifierSendMessage:
    """メッセージ送信テスト"""
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    def test_send_message_plain_text(self, mock_webhook_class):
        """プレーンテキスト送信（タイトルなし）"""
        mock_webhook = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_message("テストメッセージ")
        
        assert result is True
        mock_webhook.set_content.assert_called_once()
        mock_webhook.execute.assert_called_once()
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_send_message_with_title(self, mock_embed_class, mock_webhook_class):
        """タイトル付き埋め込みメッセージ送信"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 204
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_message(
            content="テスト内容",
            title="テストタイトル"
        )
        
        assert result is True
        mock_embed_class.assert_called_once()
        mock_webhook.add_embed.assert_called_once()
        mock_webhook.execute.assert_called_once()
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_send_message_with_url(self, mock_embed_class, mock_webhook_class):
        """URL付きメッセージ送信"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_message(
            content="テスト内容",
            title="テストタイトル",
            url="https://example.com"
        )
        
        assert result is True
        assert mock_embed.url == "https://example.com"
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    def test_send_message_http_error(self, mock_webhook_class):
        """HTTP エラー時の挙動"""
        mock_webhook = Mock()
        mock_response = Mock()
        mock_response.status_code = 400
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_message("テストメッセージ")
        
        assert result is False
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    def test_send_message_exception(self, mock_webhook_class):
        """例外発生時の挙動"""
        mock_webhook_class.side_effect = Exception("Network error")
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_message("テストメッセージ")
        
        assert result is False


class TestDiscordNotifierSendEmbed:
    """埋め込みメッセージ送信テスト"""
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_send_embed_basic(self, mock_embed_class, mock_webhook_class):
        """基本的な埋め込み送信"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_embed(
            title="テストタイトル",
            description="テスト説明"
        )
        
        assert result is True
        mock_embed_class.assert_called_once()
        mock_webhook.add_embed.assert_called_once()
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_send_embed_with_fields(self, mock_embed_class, mock_webhook_class):
        """カスタムフィールド付き埋め込み"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        fields = [
            {'name': 'フィールド1', 'value': '値1', 'inline': True},
            {'name': 'フィールド2', 'value': '値2', 'inline': False}
        ]
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_embed(
            title="テストタイトル",
            description="テスト説明",
            fields=fields
        )
        
        assert result is True
        assert mock_embed.add_embed_field.call_count == 2
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_send_embed_with_url(self, mock_embed_class, mock_webhook_class):
        """URL付き埋め込み"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_embed(
            title="テストタイトル",
            description="テスト説明",
            url="https://example.com"
        )
        
        assert result is True
        assert mock_embed.url == "https://example.com"
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_send_embed_long_text(self, mock_embed_class, mock_webhook_class):
        """長文の自動切り詰め確認"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        long_title = "a" * 300
        long_description = "b" * 5000
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_embed(
            title=long_title,
            description=long_description
        )
        
        assert result is True
        call_args = mock_embed_class.call_args
        assert len(call_args.kwargs['title']) <= 256
        assert len(call_args.kwargs['description']) <= 4096
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_send_embed_with_custom_color(self, mock_embed_class, mock_webhook_class):
        """カスタムカラー指定"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.send_embed(
            title="テストタイトル",
            description="テスト説明",
            color='ff0000'
        )
        
        assert result is True
        assert mock_embed_class.call_args.kwargs['color'] == 'ff0000'


class TestDiscordNotifierTestConnection:
    """接続テスト"""
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_connection_success(self, mock_embed_class, mock_webhook_class):
        """接続テスト成功"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.test_connection()
        
        assert result is True
        mock_webhook.execute.assert_called_once()
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    @patch('src.notifiers.discord_notifier.DiscordEmbed')
    def test_connection_failure(self, mock_embed_class, mock_webhook_class):
        """接続テスト失敗"""
        mock_webhook = Mock()
        mock_embed = Mock()
        mock_response = Mock()
        mock_response.status_code = 404
        mock_webhook.execute.return_value = mock_response
        mock_webhook_class.return_value = mock_webhook
        mock_embed_class.return_value = mock_embed
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.test_connection()
        
        assert result is False
    
    @patch('src.notifiers.discord_notifier.DiscordWebhook')
    def test_connection_exception(self, mock_webhook_class):
        """接続テストで例外発生"""
        mock_webhook_class.side_effect = Exception("Connection error")
        
        notifier = DiscordNotifier("https://discord.com/api/webhooks/123/abc")
        result = notifier.test_connection()
        
        assert result is False
