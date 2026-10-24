## gh-protocol E2E log — 2026-10-24T17:04:50Z

### gradle-build.log (tail)
Downloading https://services.gradle.org/distributions/gradle-8.10.2-bin.zip
.............10%.............20%.............30%.............40%.............50%.............60%.............70%.............80%.............90%.............100%

Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports

For more details see https://docs.gradle.org/8.10.2/release-notes.html

To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugResValues
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mapDebugSourceSetPaths
> Task :app:extractDeepLinksDebug
> Task :app:packageDebugResources
> Task :app:checkDebugAarMetadata
> Task :app:parseDebugLocalResources
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugNativeLibs
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:mergeDebugAssets
> Task :app:mergeExtDexDebug
> Task :app:mergeLibDexDebug
> Task :app:processDebugManifestForPackage
> Task :app:compressDebugAssets

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:processDebugResources
> Task :app:validateSigningDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_2-1792859361949.json

BUILD SUCCESSFUL in 2m 37s
37 actionable tasks: 37 executed
Configuration cache entry stored.

### e2e.log
== adb devices ==
== wait for emulator to reach device state ==
emulator ready after ~4s
List of devices attached
emulator-5554	device

== install APK ==
Performing Streamed Install
Success
== wait for emulator external network (needed for subscription fetch) ==
emulator has network after ~4s (icmp=no validated=8)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 2454)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
WARN: consent dialog never seen
USER           PID  PPID        VSZ    RSS WCHAN            ADDR S NAME                       
u0_a141       2454   330   13747040 167092 0                   0 S com.ghprotocol.app
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp6       0      0 [::]:5555               [::]:*                  LISTEN     
ACTIVITY MANAGER ACTIVITIES (dumpsys activity activities)
Display #0 (activities from top to bottom):
  * Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
    mLastPausedActivity: ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity t8}
    mLastNonFullscreenBounds=Rect(297, 660 - 783, 1740)
    isSleeping=false
    topResumedActivity=ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity t8}
    * Hist  #1: ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{ce75543 2454:com.ghprotocol.app/u0a141}
      Intent { act=android.intent.action.VIEW dat=ghprotocol://connect flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=false task=Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~xjEDcC9Kf4pRPQl5kFNyXw==/com.ghprotocol.app-yBQCQKOLrcwVvMY_6o2p0Q==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h842dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.72 fontWeightAdjustment=0}
        mOverrideConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h842dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.2 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h842dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.3 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} as.2 ?fontWeightAdjustment}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=false
      windows=[Window{da6ef84 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=true mVisible=true mClientVisible=true reportedDrawn=true reportedVisible=true
      mNumInterestingWindows=1 mNumDrawnWindows=1 allDrawn=true lastAllDrawn=true)
      startingData=null firstWindowDrawn=true mIsExiting=false
      nowVisible=true lastVisibleTime=-20m14s233ms
--
      mCameraCompatControlState=hidden
      mCameraCompatControlEnabled=false
    * Hist  #0: ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity t8}
      packageName=com.ghprotocol.app processName=com.ghprotocol.app
      launchedFromUid=2000 launchedFromPackage=com.android.shell launchedFromFeature=null userId=0
      app=ProcessRecord{ce75543 2454:com.ghprotocol.app/u0a141}
      Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity }
      rootOfTask=true task=Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}
      taskAffinity=10141:com.ghprotocol.app
      mActivityComponent=com.ghprotocol.app/.MainActivity
      baseDir=/data/app/~~xjEDcC9Kf4pRPQl5kFNyXw==/com.ghprotocol.app-yBQCQKOLrcwVvMY_6o2p0Q==/base.apk
      dataDir=/data/user/0/com.ghprotocol.app
      stateNotNeeded=false componentSpecified=false mActivityType=standard
      compat={420dpi} labelRes=0x7f0a000f icon=0x7f090000 theme=0x7f0b000a
      mLastReportedConfigurations:
        mGlobalConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h842dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} s.36 fontWeightAdjustment=0}
        mOverrideConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h842dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} s.1 fontWeightAdjustment=0}
      CurrentConfiguration={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h842dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=standard mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.3 fontWeightAdjustment=0}
      RequestedOverrideConfiguration={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=undefined mDisplayWindowingMode=undefined mActivityType=standard mAlwaysOnTop=undefined mRotation=undefined} as.2 ?fontWeightAdjustment}
      taskDescription: label="null" icon=null iconResource=/0 iconFilename=null primaryColor=ff212121
--
      mActivityType=standard
      mImeInsetsFrozenUntilStartInput=true
      windows=[Window{74d1fa3 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}]
      windowType=2
      mOccludesParent=true
      overrideOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      requestedOrientation=SCREEN_ORIENTATION_UNSPECIFIED
      mVisibleRequested=false mVisible=false mClientVisible=false reportedDrawn=false reportedVisible=false
      mAppStopped=true
      startingWindow=null startingSurface=null startingDisplayed=false startingMoved=true mVisibleSetFromTransferredStartingWindow=false
      resizeMode=RESIZE_MODE_RESIZEABLE_VIA_SDK_VERSION
--

  Resumed activities in task display areas (from top to bottom):
    Resumed: ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity t8}

  ResumedActivity: ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity t8}

ActivityTaskSupervisor state:
  topDisplayFocusedRootTask=Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}
  Display: mDisplayId=0 (organized)
    init=1080x2400 420dpi mMinSizeOfResizeableTaskDp=220 cur=1080x2400 app=1080x2274 rng=1080x1017-2274x2211
    deferred=false mLayoutNeeded=false mTouchExcludeRegion=SkRegion((0,0,1080,2400))

  mLastOrientationSource=WindowedMagnification:0:31@104728628
  deepestLastOrientationSource=ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity t8}
  overrideConfig={1.0 ?mcc0mnc [en_US] ldltr sw411dp w411dp h842dp 420dpi nrml long port finger qwerty/v/v -nav/h winConfig={ mBounds=Rect(0, 0 - 1080, 2400) mAppBounds=Rect(0, 0 - 1080, 2274) mMaxBounds=Rect(0, 0 - 1080, 2400) mDisplayRotation=ROTATION_0 mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=ROTATION_0} as.2 s.64 fontWeightAdjustment=0}
  mLayoutSeq=86
  mCurrentFocus=Window{67f317 u0 Application Not Responding: system}
  mFocusedApp=ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity t8}

  mHoldScreenWindow=null
  mObscuringWindow=Window{da6ef84 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
  mLastWakeLockHoldingWindow=null
  mLastWakeLockObscuringWindow=null

  displayId=0
  mWallpaperTarget=null
  mLastWallpaperX=0.0 mLastWallpaperY=0.5

  Display areas in top down Z order:
--
    TaskDisplayArea DefaultTaskDisplayArea
      overrideConfig={0.0 ?mcc0mnc ?localeList ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?ldr ?wideColorGamut ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/? winConfig={ mBounds=Rect(0, 0 - 0, 0) mAppBounds=null mMaxBounds=Rect(0, 0 - 0, 0) mDisplayRotation=undefined mWindowingMode=fullscreen mDisplayWindowingMode=fullscreen mActivityType=undefined mAlwaysOnTop=undefined mRotation=undefined} ?fontWeightAdjustment}
      mPreferredTopFocusableRootTask=Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}
      mLastFocusedRootTask=Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}
      Application tokens in top down Z order:
      * Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app U=0 visible=true visibleRequested=true mode=fullscreen translucent=false sz=2}
        bounds=[0,0][1080,2400]
        * ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity t8}
        * ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity t8}
      * Task{d24bbd2 #1 type=home U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
        bounds=[0,0][1080,2400]
        * Task{cb2a160 #7 type=home I=com.android.launcher3/.uioverrides.QuickstepLauncher U=0 rootTaskId=1 visible=false visibleRequested=false mode=fullscreen translucent=true sz=1}
          bounds=[0,0][1080,2400]
          * ActivityRecord{7747163 u0 com.android.launcher3/.uioverrides.QuickstepLauncher t7}
      * Task{8d45c8a #2 type=undefined U=0 visible=false visibleRequested=false mode=fullscreen translucent=true sz=2}
        bounds=[0,0][1080,2400]
        * Task{5f50f18 #4 type=undefined U=0 rootTaskId=2 visible=false visibleRequested=false mode=multi-window translucent=true sz=0}
--
    mBottomGestureHost=Window{47a19a5 u0 NavigationBar0}
    mFocusedWindow=Window{67f317 u0 Application Not Responding: system}
    mTopFullscreenOpaqueWindowState=Window{da6ef84 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mNavBarColorWindowCandidate=Window{67f317 u0 Application Not Responding: system}
    mNavBarBackgroundWindow=Window{da6ef84 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mLastStatusBarAppearanceRegions=
      AppearanceRegion{ bounds=[0,0][1080,2400]}
    mLastLetterboxDetails=
    mStatusBarBackgroundWindows=
      Window{da6ef84 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}
    mTopIsFullscreen=false
    mForceShowNavigationBarEnabled=false mAllowLockscreenWhenOn=false
    mRemoteInsetsControllerControlsSystemBars=false
    mDecorInsetsInfo:
      ROTATION_0={nonDecorInsets=[0,0][0,126], configInsets=[0,63][0,126], nonDecorFrame=[0,0][1080,2274], configFrame=[0,63][1080,2274]}
      ROTATION_90={nonDecorInsets=[0,0][126,0], configInsets=[0,63][126,0], nonDecorFrame=[0,0][2274,1080], configFrame=[0,63][2274,1080]}
      ROTATION_180={nonDecorInsets=[0,0][0,126], configInsets=[0,63][0,126], nonDecorFrame=[0,0][1080,2274], configFrame=[0,63][1080,2274]}
      ROTATION_270={nonDecorInsets=[126,0][0,0], configInsets=[126,63][0,0], nonDecorFrame=[126,0][2400,1080], configFrame=[126,63][2400,1080]}
--
        (multi-window) Task{359a2fb #3 type=undefined}
        (multi-window) Task{5f50f18 #4 type=undefined}
        (fullscreen) Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}

  VisibleActivityProcess:[ ProcessRecord{ce75543 2454:com.ghprotocol.app/u0a141}]
  NumNonAppVisibleWindowUidMap:[ 10118:2 1000:2]
=== E2E FAILED: tunnel not up (xray/:10808) ===


### e2e-logcat.log (crashes + app + vpn, tail)
ss timeout for ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity t8}
10-24 16:42:09.421   547   573 W ActivityTaskManager: Activity pause timeout for ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity t8}
10-24 16:42:09.445   547   570 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{925f725 Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0x4bb8b45 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{9f75023 Task{d24bbd2 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0xaedef06 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 16:42:09.661  2454  2454 W .ghprotocol.app: Verification of void androidx.collection.ArraySet.<init>(int) took 217.233ms (87.46 bytecodes/s) (1712B approximate peak alloc)
10-24 16:42:09.794  2454  2454 W .ghprotocol.app: Verification of int androidx.collection.internal.ContainerHelpersKt.binarySearch(long[], int, long) took 122.319ms (269.79 bytecodes/s) (2160B approximate peak alloc)
10-24 16:42:10.483   957   994 V WindowManagerShell: onTransitionReady android.os.BinderProxy@5b45f53: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=STARTING_WINDOW_TRANSFER|FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity)/@0xf2761a8 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity)/@0x375f4c1 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 16:42:11.587   547   570 V WindowManager: Sent Transition #7 createdAt=10-24 16:42:07.703 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=589034 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{925f725 Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{6859e14 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-24 16:42:11.649   547   570 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=STARTING_WINDOW_TRANSFER|FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{d7a614a u0 com.ghprotocol.app/.MainActivity)/@0x6fbf395 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK|IS_BEHIND_STARTING_WINDOW leash=Surface(name=ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity)/@0x325874c sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-24 16:42:12.443  2454  2454 W .ghprotocol.app: Verification of void androidx.activity.ComponentActivity.<init>() took 263.048ms (900.97 bytecodes/s) (7816B approximate peak alloc)
10-24 16:42:22.285   547   573 W ActivityTaskManager: Activity stop timeout for ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity t8}
10-24 16:42:22.868  2454  2454 W .ghprotocol.app: Verification of void androidx.compose.ui.platform.AndroidComposeView.<init>(android.content.Context, kotlin.coroutines.CoroutineContext) took 119.466ms (7181.93 bytecodes/s) (30440B approximate peak alloc)
10-24 16:42:28.382  2454  2462 W .ghprotocol.app: Suspending all threads took: 36.192ms
10-24 16:42:28.707  2454  2462 I .ghprotocol.app: Background concurrent copying GC freed 8045(926KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 3156KB/6312KB, paused 650us,43.464ms total 2.758s
10-24 16:42:35.686  2454  2454 W .ghprotocol.app: Verification of void androidx.navigation.compose.NavHostKt.NavHost(androidx.navigation.NavHostController, androidx.navigation.NavGraph, androidx.compose.ui.Modifier, androidx.compose.ui.Alignment, kotlin.jvm.functions.Function1, kotlin.jvm.functions.Function1, kotlin.jvm.functions.Function1, kotlin.jvm.functions.Function1, kotlin.jvm.functions.Function1, androidx.compose.runtime.Composer, int, int) took 152.805ms (14338.45 bytecodes/s) (57464B approximate peak alloc)
10-24 16:42:35.971  2454  2611 W .ghprotocol.app: Long monitor contention with owner DefaultDispatcher-worker-2 (2612) at javax.net.SocketFactory javax.net.ssl.SSLSocketFactory.getDefault()(SSLSocketFactory.java:156) waiters=0 in javax.net.SocketFactory javax.net.ssl.SSLSocketFactory.getDefault() for 265ms
10-24 16:42:37.327  2454  2612 W .ghprotocol.app: Verification of java.lang.String com.ghprotocol.app.domain.ProbeResult.toString() took 135.610ms (383.45 bytecodes/s) (1912B approximate peak alloc)
10-24 16:42:38.750  2454  2454 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 16:42:38.750  2454  2454 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-24 16:42:38.750  2454  2454 W .ghprotocol.app: and incorrect proguard optimizations.
10-24 16:42:38.757  2454  2454 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 16:42:38.770  2454  2454 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 16:42:38.775  2454  2454 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-24 16:42:38.778  2454  2454 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-24 16:42:39.347  2454  2454 W .ghprotocol.app: Verification of androidx.compose.animation.core.KeyframesSpec androidx.compose.animation.core.AnimationSpecKt.keyframes(kotlin.jvm.functions.Function1) took 103.624ms (135.10 bytecodes/s) (1608B approximate peak alloc)
10-24 16:42:43.709  2613  2613 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:42:44.155  2613  2613 I AndroidRuntime: Using default boot image
10-24 16:42:44.164  2613  2613 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:42:44.256   547  2010 D CoreBackPreview: Window{74d1fa3 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@2fa9907, mPriority=0, mIsAnimationCallback=false}
10-24 16:42:47.431   547   608 I AppsFilter: interaction: PackageSetting{8d90ca6 com.ghprotocol.app/10141} -> PackageSetting{4a926e7 com.android.inputmethod.latin/10107} BLOCKED
10-24 16:42:51.730  2454  2454 W .ghprotocol.app: Verification of androidx.compose.ui.layout.MeasureResult androidx.compose.foundation.layout.FlowLayoutKt.breakDownItems-di9J0FM(androidx.compose.ui.layout.MeasureScope, androidx.compose.foundation.layout.FlowLineMeasurePolicy, java.util.Iterator, float, float, long, int, int, androidx.compose.foundation.layout.FlowLayoutOverflowState) took 102.151ms (13812.81 bytecodes/s) (31912B approximate peak alloc)
10-24 16:42:53.020   547  2623 E ActivityManager:   48% 2454/com.ghprotocol.app: 37% user + 11% kernel / faults: 637 minor 6 major
10-24 16:42:53.629  2613  2613 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:42:54.645   547   608 I AppsFilter: interaction: PackageSetting{e7a0396 com.ghprotocol.app/10141} -> PackageSetting{30f6b17 com.android.calendar/10101} BLOCKED
10-24 16:42:58.170  2613  2613 D AndroidRuntime: Shutting down VM
10-24 16:42:58.223   547   573 I BLASTSyncEngine: Unfinished container: Task{bcd6a18 #8 type=standard A=10141:com.ghprotocol.app}
10-24 16:43:06.381   547  1648 D CoreBackPreview: Window{e277942 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@4193802, mPriority=0, mIsAnimationCallback=false}
10-24 16:43:10.667   547   608 I AppsFilter: interaction: PackageSetting{e7a0396 com.ghprotocol.app/10141} -> PackageSetting{c16090c com.android.camera2/10105} BLOCKED
10-24 16:43:15.277  2454  2462 I .ghprotocol.app: Background young concurrent copying GC freed 17398(1308KB) AllocSpace objects, 0(0B) LOS objects, 22% free, 4899KB/6312KB, paused 209.205ms,81us total 3.988s
10-24 16:43:20.661   547  1016 I WindowManager: finishDrawing of relaunch: Window{e277942 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity} 23886ms
10-24 16:43:20.957   547   570 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1m15s278ms
10-24 16:43:21.672   547  1512 D CoreBackPreview: Window{b016963 u0 Splash Screen com.ghprotocol.app}: Setting back callback null
10-24 16:43:22.301   547  2143 W InputManager-JNI: Input channel object 'b016963 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-24 16:43:22.939  2454  2803 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-24 16:43:23.236  2454  2803 W .ghprotocol.app: Verification of androidx.profileinstaller.DeviceProfileWriter androidx.profileinstaller.DeviceProfileWriter.transcodeIfNeeded() took 232.706ms (348.08 bytecodes/s) (3608B approximate peak alloc)
10-24 16:43:23.693  2454  2803 W .ghprotocol.app: Verification of java.lang.Object androidx.concurrent.futures.AbstractResolvableFuture.get() took 142.342ms (723.60 bytecodes/s) (3912B approximate peak alloc)
10-24 16:43:24.333   547  1018 D CoreBackPreview: Window{e277942 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback null
10-24 16:43:24.436   547   629 W InputManager-JNI: Input channel object 'e277942 com.ghprotocol.app/com.ghprotocol.app.MainActivity (client)' was disposed without first being removed with the input manager!
10-24 16:43:26.089   547   629 I ActivityTaskManager: Activity reported stop, but no longer stopping: ActivityRecord{3c1072c u0 com.ghprotocol.app/.MainActivity t8} STOPPED
10-24 16:43:35.901   547  2143 D CoreBackPreview: Window{da6ef84 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@16c3310, mPriority=0, mIsAnimationCallback=false}
10-24 16:43:40.722  2855  2855 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:43:41.564  2855  2855 I AndroidRuntime: Using default boot image
10-24 16:43:41.589  2855  2855 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:43:47.901   547  2863 E ActivityManager:   43% 2454/com.ghprotocol.app: 35% user + 8.2% kernel / faults: 464 minor
10-24 16:43:50.696  2855  2855 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:43:53.346  2855  2855 D AndroidRuntime: Shutting down VM
10-24 16:44:06.206   547   608 I AppsFilter: interaction: PackageSetting{e7a0396 com.ghprotocol.app/10141} -> PackageSetting{7f78634 com.android.rkpdapp/10131} BLOCKED
10-24 16:44:08.299   547   608 I AppsFilter: interaction: PackageSetting{e7a0396 com.ghprotocol.app/10141} -> PackageSetting{6d368da com.android.rkpdapp/10131} BLOCKED
10-24 16:44:28.692  3031  3031 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:44:29.047  3031  3031 I AndroidRuntime: Using default boot image
10-24 16:44:29.051  3031  3031 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:44:31.690   547  3041 E ActivityManager:   2.9% 2454/com.ghprotocol.app: 1.7% user + 1.1% kernel / faults: 97 minor
10-24 16:44:36.035  3031  3031 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:44:40.672  3031  3031 D AndroidRuntime: Shutting down VM
10-24 16:45:02.285  2993  2993 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:45:23.807  3236  3236 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:45:24.470  3236  3236 I AndroidRuntime: Using default boot image
10-24 16:45:24.472  3236  3236 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:45:31.059  3236  3236 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:45:35.440  3236  3236 D AndroidRuntime: Shutting down VM
10-24 16:45:43.027  3198  3198 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:46:16.042  3426  3426 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:46:16.357  3426  3426 I AndroidRuntime: Using default boot image
10-24 16:46:16.358  3426  3426 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:46:22.521  3426  3426 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:46:25.854  3426  3426 D AndroidRuntime: Shutting down VM
10-24 16:46:26.419  3324  3324 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:46:54.740  3523  3523 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:47:01.525  3670  3670 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:47:01.921  3670  3670 I AndroidRuntime: Using default boot image
10-24 16:47:01.921  3670  3670 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:47:10.049  3670  3670 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:47:13.092  3670  3670 D AndroidRuntime: Shutting down VM
10-24 16:47:33.602  3676  3676 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:47:47.307  3876  3876 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:47:47.528  3876  3876 I AndroidRuntime: Using default boot image
10-24 16:47:47.530  3876  3876 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:47:52.360  3876  3876 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:47:55.233  3876  3876 D AndroidRuntime: Shutting down VM
10-24 16:47:58.703  3830  3830 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:48:19.685  3911  3911 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:48:30.195  4000  4000 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:48:30.476  4000  4000 I AndroidRuntime: Using default boot image
10-24 16:48:30.477  4000  4000 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:48:37.127  4000  4000 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:48:39.559  4000  4000 D AndroidRuntime: Shutting down VM
10-24 16:48:44.937  3985  3985 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:49:06.559  4068  4068 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:49:12.779  4136  4136 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:49:13.052  4136  4136 I AndroidRuntime: Using default boot image
10-24 16:49:13.054  4136  4136 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:49:20.117  4136  4136 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:49:22.559  4136  4136 D AndroidRuntime: Shutting down VM
10-24 16:49:39.367  4138  4138 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:49:59.037  4288  4288 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:49:59.230  4288  4288 I AndroidRuntime: Using default boot image
10-24 16:49:59.230  4288  4288 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:50:04.692  4288  4288 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:50:07.044  4288  4288 D AndroidRuntime: Shutting down VM
10-24 16:50:12.127  4223  4223 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:50:36.685  4318  4318 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:50:41.035  4388  4388 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:50:41.270  4388  4388 I AndroidRuntime: Using default boot image
10-24 16:50:41.271  4388  4388 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:50:46.255  4388  4388 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:50:48.432  4388  4388 D AndroidRuntime: Shutting down VM
10-24 16:51:02.846  4392  4392 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:51:21.586  4541  4541 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:51:21.943  4541  4541 I AndroidRuntime: Using default boot image
10-24 16:51:21.945  4541  4541 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:51:28.575  4541  4541 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:51:31.971  4541  4541 D AndroidRuntime: Shutting down VM
10-24 16:51:32.571  4485  4485 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:51:54.419  4570  4570 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:52:04.755  4659  4659 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:52:04.976  4659  4659 I AndroidRuntime: Using default boot image
10-24 16:52:04.977  4659  4659 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:52:11.156  4659  4659 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:52:13.724  4659  4659 D AndroidRuntime: Shutting down VM
10-24 16:52:22.571  4641  4641 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:52:48.237  4810  4810 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:52:48.458  4810  4810 I AndroidRuntime: Using default boot image
10-24 16:52:48.459  4810  4810 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:52:51.907  4738  4738 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:52:54.183  4810  4810 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:52:57.635  4810  4810 D AndroidRuntime: Shutting down VM
10-24 16:53:22.877  4825  4825 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:53:27.647  4910  4910 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:53:27.826  4910  4910 I AndroidRuntime: Using default boot image
10-24 16:53:27.828  4910  4910 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:53:34.023  4910  4910 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:53:36.253  4910  4910 D AndroidRuntime: Shutting down VM
10-24 16:53:50.021  4914  4914 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:54:07.159  5057  5057 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:54:07.363  5057  5057 I AndroidRuntime: Using default boot image
10-24 16:54:07.363  5057  5057 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:54:12.371  5057  5057 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:54:15.241  5057  5057 D AndroidRuntime: Shutting down VM
10-24 16:54:19.553  5004  5004 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:54:37.954  5087  5087 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:54:45.703  5169  5169 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:54:45.912  5169  5169 I AndroidRuntime: Using default boot image
10-24 16:54:45.913  5169  5169 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:54:51.871  5169  5169 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:54:55.001  5169  5169 D AndroidRuntime: Shutting down VM
10-24 16:55:08.703  5154  5154 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:55:27.729  5298  5298 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:55:27.966  5298  5298 I AndroidRuntime: Using default boot image
10-24 16:55:27.966  5298  5298 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:55:32.432  5298  5298 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:55:35.319  5298  5298 D AndroidRuntime: Shutting down VM
10-24 16:55:38.945  5239  5239 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:56:00.750  5323  5323 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:56:07.058  5417  5417 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:56:07.315  5417  5417 I AndroidRuntime: Using default boot image
10-24 16:56:07.315  5417  5417 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:56:13.172  5417  5417 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:56:15.301  5417  5417 D AndroidRuntime: Shutting down VM
10-24 16:56:25.589  5407  5407 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:56:42.812  5491  5491 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:56:49.837  5570  5570 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:56:50.137  5570  5570 I AndroidRuntime: Using default boot image
10-24 16:56:50.144  5570  5570 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:56:55.034  5570  5570 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:56:57.841  5570  5570 D AndroidRuntime: Shutting down VM
10-24 16:57:07.286  5558  5558 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:57:25.474  5651  5651 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:57:31.230  5721  5721 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:57:31.551  5721  5721 I AndroidRuntime: Using default boot image
10-24 16:57:31.551  5721  5721 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:57:36.287  5721  5721 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:57:38.986  5721  5721 D AndroidRuntime: Shutting down VM
10-24 16:57:47.382  5723  5723 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:58:06.439  5806  5806 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:58:12.854  5883  5883 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:58:13.067  5883  5883 I AndroidRuntime: Using default boot image
10-24 16:58:13.076  5883  5883 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:58:19.065  5883  5883 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:58:22.254  5883  5883 D AndroidRuntime: Shutting down VM
10-24 16:58:28.918  5878  5878 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:58:48.376  5964  5964 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:58:55.142  6040  6040 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:58:55.337  6040  6040 I AndroidRuntime: Using default boot image
10-24 16:58:55.338  6040  6040 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:58:57.808  2454  2462 W .ghprotocol.app: Suspending all threads took: 19.384ms
10-24 16:58:58.042  2454  2462 W .ghprotocol.app: Cleared Reference was only reachable from finalizer (only reported once)
10-24 16:58:58.099  2454  2462 I .ghprotocol.app: Background concurrent copying GC freed 19631(878KB) AllocSpace objects, 0(0B) LOS objects, 49% free, 5408KB/10MB, paused 6.920ms,19.819ms total 1.662s
10-24 16:59:02.137  6040  6040 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:59:05.271  6040  6040 D AndroidRuntime: Shutting down VM
10-24 16:59:10.220  6030  6030 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:59:38.401  6114  6114 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 16:59:39.144  6194  6194 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 16:59:39.404  6194  6194 I AndroidRuntime: Using default boot image
10-24 16:59:39.404  6194  6194 I AndroidRuntime: Leaving lock profiling enabled
10-24 16:59:44.494  6194  6194 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 16:59:46.911  6194  6194 D AndroidRuntime: Shutting down VM
10-24 17:00:02.208  6199  6199 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:00:21.109  6355  6355 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:00:21.341  6355  6355 I AndroidRuntime: Using default boot image
10-24 17:00:21.341  6355  6355 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:00:24.432  6290  6290 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:00:26.614  6355  6355 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:00:29.253  6355  6355 D AndroidRuntime: Shutting down VM
10-24 17:00:46.697  6370  6370 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:01:00.045  6509  6509 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:01:00.291  6509  6509 I AndroidRuntime: Using default boot image
10-24 17:01:00.291  6509  6509 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:01:05.823  6509  6509 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:01:08.908  6509  6509 D AndroidRuntime: Shutting down VM
10-24 17:01:13.821  6452  6452 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:01:37.967  6543  6543 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:01:41.085  6621  6621 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:01:41.279  6621  6621 I AndroidRuntime: Using default boot image
10-24 17:01:41.279  6621  6621 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:01:45.668  6621  6621 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:01:47.950  6621  6621 D AndroidRuntime: Shutting down VM
10-24 17:02:01.478  6625  6625 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:02:18.414  6770  6770 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:02:18.675  6770  6770 I AndroidRuntime: Using default boot image
10-24 17:02:18.675  6770  6770 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:02:24.637  6770  6770 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:02:27.426  6770  6770 D AndroidRuntime: Shutting down VM
10-24 17:02:30.795  6715  6715 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:02:50.651  6799  6799 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:02:57.970  6890  6890 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:02:58.191  6890  6890 I AndroidRuntime: Using default boot image
10-24 17:02:58.194  6890  6890 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:03:03.131  6890  6890 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:03:05.778  6890  6890 D AndroidRuntime: Shutting down VM
10-24 17:03:11.192  6879  6879 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:03:35.477  6960  6960 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.
10-24 17:03:40.582  7036  7036 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-24 17:03:40.873  7036  7036 I AndroidRuntime: Using default boot image
10-24 17:03:40.873  7036  7036 I AndroidRuntime: Leaving lock profiling enabled
10-24 17:03:46.765  7036  7036 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-24 17:03:49.532  7036  7036 D AndroidRuntime: Shutting down VM
10-24 17:04:07.383  7040  7040 I AndroidRuntime: VM exiting with result code 0, cleanup skipped.


