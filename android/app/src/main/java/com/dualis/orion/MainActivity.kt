package com.dualis.orion

import android.annotation.SuppressLint
import android.app.AlertDialog
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.view.View
import android.webkit.*
import android.widget.Button
import android.widget.EditText
import android.widget.ImageButton
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.Toast
import androidx.activity.OnBackPressedCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout

class MainActivity : AppCompatActivity() {

    private lateinit var webView: WebView
    private lateinit var swipeRefresh: SwipeRefreshLayout
    private lateinit var progressBar: ProgressBar
    private lateinit var errorLayout: LinearLayout
    private lateinit var btnRetry: Button
    private lateinit var btnConfigure: Button
    private lateinit var btnSettings: ImageButton

    private var filePathCallback: ValueCallback<Array<Uri>>? = null

    private val filePickerLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (filePathCallback != null) {
            val data: Intent? = result.data
            val results: Array<Uri>? = when {
                result.resultCode == RESULT_OK && data?.data != null -> arrayOf(data.data!!)
                result.resultCode == RESULT_OK && data?.clipData != null -> {
                    val clipData = data.clipData!!
                    Array(clipData.itemCount) { i -> clipData.getItemAt(i).uri }
                }
                else -> null
            }
            filePathCallback?.onReceiveValue(results)
            filePathCallback = null
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webView)
        swipeRefresh = findViewById(R.id.swipeRefreshLayout)
        progressBar = findViewById(R.id.progressBar)
        errorLayout = findViewById(R.id.errorLayout)
        btnRetry = findViewById(R.id.btnRetry)
        btnConfigure = findViewById(R.id.btnConfigure)
        btnSettings = findViewById(R.id.btnSettings)

        setupWebView()
        setupListeners()

        val savedUrl = getServerUrl()
        if (savedUrl.contains("10.0.2.2") || savedUrl.isBlank()) {
            showChangeUrlDialog(isFirstRun = true)
        } else {
            loadAppUrl()
        }
    }

    private fun getServerUrl(): String {
        val prefs = getSharedPreferences("orion_config", Context.MODE_PRIVATE)
        return prefs.getString("server_url", getString(R.string.default_server_url)) 
            ?: getString(R.string.default_server_url)
    }

    private fun setServerUrl(newUrl: String) {
        var formatted = newUrl.trim()
        if (!formatted.startsWith("http://") && !formatted.startsWith("https://")) {
            formatted = "https://$formatted"
        }
        val prefs = getSharedPreferences("orion_config", Context.MODE_PRIVATE)
        prefs.edit().putString("server_url", formatted).apply()
        Toast.makeText(this, "Servidor salvo: $formatted", Toast.LENGTH_SHORT).show()
        loadAppUrl()
    }

    private fun loadAppUrl() {
        val url = getServerUrl()
        if (url.contains("10.0.2.2") || url.isBlank()) {
            errorLayout.visibility = View.VISIBLE
            webView.visibility = View.GONE
            return
        }
        errorLayout.visibility = View.GONE
        webView.visibility = View.VISIBLE
        webView.loadUrl(url)
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        webView.setBackgroundColor(Color.parseColor("#080B11"))

        val settings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.useWideViewPort = true
        settings.loadWithOverviewMode = true
        settings.allowFileAccess = true
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        settings.userAgentString = settings.userAgentString + " ORION_Android_App"

        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                super.onPageStarted(view, url, favicon)
                progressBar.visibility = View.VISIBLE
                errorLayout.visibility = View.GONE
                webView.visibility = View.VISIBLE
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                progressBar.visibility = View.GONE
                swipeRefresh.isRefreshing = false
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)
                if (request?.isForMainFrame == true) {
                    progressBar.visibility = View.GONE
                    swipeRefresh.isRefreshing = false
                    webView.visibility = View.GONE
                    errorLayout.visibility = View.VISIBLE
                }
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                progressBar.progress = newProgress
                if (newProgress >= 100) {
                    progressBar.visibility = View.GONE
                }
            }

            override fun onShowFileChooser(
                webView: WebView?,
                filePathCallback: ValueCallback<Array<Uri>>?,
                fileChooserParams: FileChooserParams?
            ): Boolean {
                this@MainActivity.filePathCallback?.onReceiveValue(null)
                this@MainActivity.filePathCallback = filePathCallback

                val intent = fileChooserParams?.createIntent() ?: Intent(Intent.ACTION_GET_CONTENT).apply {
                    type = "*/*"
                    addCategory(Intent.CATEGORY_OPENABLE)
                }
                try {
                    filePickerLauncher.launch(intent)
                } catch (e: Exception) {
                    this@MainActivity.filePathCallback = null
                    return false
                }
                return true
            }
        }
    }

    private fun setupListeners() {
        swipeRefresh.setOnRefreshListener {
            webView.reload()
        }

        btnRetry.setOnClickListener {
            loadAppUrl()
        }

        btnConfigure.setOnClickListener {
            showChangeUrlDialog(isFirstRun = false)
        }

        btnSettings.setOnClickListener {
            showChangeUrlDialog(isFirstRun = false)
        }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView.canGoBack()) {
                    webView.goBack()
                } else {
                    finish()
                }
            }
        })
    }

    private fun showChangeUrlDialog(isFirstRun: Boolean = false) {
        val current = getServerUrl().replace("http://10.0.2.2:8501", "")
        val input = EditText(this).apply {
            hint = "ex: orion-dualis.streamlit.app"
            setText(current)
            setSelection(text.length)
        }

        val dialog = AlertDialog.Builder(this)
            .setTitle("Link do Sistema ORION")
            .setMessage("Cole o link da nuvem gerado no Streamlit Cloud ou o IP do computador:")
            .setView(input)
            .setPositiveButton("Salvar e Conectar") { _, _ ->
                val newUrl = input.text.toString().trim()
                if (newUrl.isNotBlank()) {
                    setServerUrl(newUrl)
                } else {
                    loadAppUrl()
                }
            }

        if (!isFirstRun) {
            dialog.setNegativeButton("Cancelar", null)
        } else {
            dialog.setCancelable(false)
        }

        dialog.show()
    }
}
