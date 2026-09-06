package app.muscleparadise.client;

import android.app.Activity;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;

/**
 * WebView shell for the Muscle Paradise athlete app.
 *
 * The backend lives on the gym PC; the phone points at it over the LAN. On first
 * launch the athlete enters the server address once, then the shell loads the
 * athlete PWA (/client.html) from it. Cleartext is allowed because gyms run on
 * private LAN addresses.
 */
public class MainActivity extends Activity {
    private static final String PREFS = "mp-client";
    private static final String KEY_URL = "server_url";
    private static final String DEFAULT_URL = "http://10.0.2.2:8751";

    private WebView webView;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.parseColor("#0B0F14"));

        SharedPreferences prefs = getSharedPreferences(PREFS, MODE_PRIVATE);
        String base = prefs.getString(KEY_URL, null);
        if (base == null || base.isEmpty()) {
            setContentView(buildSetup(prefs));
        } else {
            setContentView(buildWebView(base));
        }
    }

    private View buildSetup(SharedPreferences prefs) {
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(48, 96, 48, 48);
        layout.setBackgroundColor(Color.parseColor("#0B0F14"));

        EditText input = new EditText(this);
        input.setHint("http://192.168.1.10:8751");
        input.setTextColor(Color.WHITE);
        input.setHintTextColor(Color.GRAY);
        layout.addView(input, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        Button save = new Button(this);
        save.setText("اتصال");
        save.setOnClickListener(v -> {
            String url = input.getText().toString().trim();
            if (url.isEmpty()) {
                url = DEFAULT_URL;
            }
            prefs.edit().putString(KEY_URL, url).apply();
            setContentView(buildWebView(url));
        });
        layout.addView(save);
        return layout;
    }

    private View buildWebView(String base) {
        webView = new WebView(this);
        WebSettings s = webView.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl(base + "/client.html");
        return webView;
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
