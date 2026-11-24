# Лабораторная работа №3 <br> Автоматизация UI-тестов и построение CI/CD-пайплайна с блокирующими quality gates

**Выполнил:** Шпак Никита  
**Группа:** ВТ-231

[![Lab3 CI](https://github.com/ShpakN/testback/actions/workflows/ci.yml/badge.svg?branch=my-pr)](https://github.com/ShpakN/testback/actions/workflows/ci.yml)
## 1. Цель работы

Освоить UI-автоматизацию, паттерны проектирования тестов, встраивание тестов в пайплайн непрерывной интеграции и настройку блокирующих quality gates, при которых падение тестов останавливает сборку и релиз.

## 2. Описание проекта

Для выполнения лабораторной работы использован интернет-магазин Edgistify, построенный на React и Node.js (исходный код: github.com/Sajid788/edgistify-Assignment).
Приложение позволяет пользователям регистрироваться, авторизоваться, просматривать каталог и искать товары, добавлять их в корзину, оформлять заказ и выходить из системы. Для тестирования развёрнуты три компонента: frontend (Vite, порт 5173), backend (Express, порт 5000) и база данных MongoDB.
Исходный код проекта расположен в каталоге [edgistify-Assignment/](https://github.com/Sajid788/edgistify-Assignment), тестовый проект — в [edgistify-Assignment/e2e/](https://github.com/ShpakN/testback/tree/main/e2e).

## Используемые технологии

| Технология | Назначение |
|---|---|
| TypeScript | язык разработки тестов и Page Object-классов |
| Playwright |автоматизация браузера и E2E-тестирование |
| Chromium | браузер, используемый в CI |
| React | frontend приложения |
| Vite | сборка и запуск frontend |
| Node.js | среда выполнения тестов и серверной части |
| Express | backend-приложение |
| MongoDB| хранение данных приложения |
| Vitest | unit-тестирование |
| Node.js Test Runner | запуск интеграционных тестов |
| Supertest | проверка HTTP API |
| GitHub Actions | запуск CI/CD-пайплайна |

## Реализованные E2E-тесты

| № | Спецификация | Сценарий | Результат |
|:--:|---|---|:--:|
| 1 | `01-registration.spec.ts` | Успешная регистрация и переход на страницу входа | PASSED |
| 2 | `01-registration.spec.ts` | Повторная регистрация с существующим email — ошибка | PASSED |
| 3 | `01-registration.spec.ts` | Пустые поля блокируются HTML5-валидацией | PASSED |
| 4 | `02-login-logout.spec.ts` | Успешный логин и появление кнопки Logout | PASSED |
| 5 | `02-login-logout.spec.ts` | Логин с неверным паролем — Login failed | PASSED |
| 6 | `02-login-logout.spec.ts` | Логин несуществующего пользователя — User not found | PASSED |
| 7 | `02-login-logout.spec.ts` | Закрытые маршруты редиректят на логин | PASSED |
| 8 | `02-login-logout.spec.ts` | Logout очищает токен и возвращает на `/login` | PASSED |
| 9 | `02-login-logout.spec.ts` | После Logout защищённый маршрут недоступен | PASSED |
| 10 | `03-product-search.spec.ts` | Каталог загружается и содержит товары | PASSED |
| 11 | `03-product-search.spec.ts` | Поиск по фрагменту названия находит товар | PASSED |
| 12 | `03-product-search.spec.ts` | Переход в карточку товара по клику | PASSED |
| 13 | `03-product-search.spec.ts` | Фильтр по названию скрывает несовпадающие товары | PASSED |
| 14 | `04-cart.spec.ts` | После логина товар добавляется и виден в корзине | PASSED |
| 15 | `04-cart.spec.ts` | Гость не может добавить в корзину | PASSED |
| 16 | `04-cart.spec.ts` | Удаление товара из корзины | PASSED |
| 17 | `05-checkout.spec.ts` | Полный happy path: каталог → корзина → checkout → `/placed` | PASSED |
| 18 | `05-checkout.spec.ts` | Checkout с пустой корзиной не создаёт заказ | PASSED |
| **Итого** | **5 спецификаций** | **18 сценариев** | **18/18 PASSED** |

Тесты выполняют действия через интерфейс браузера и проверяют результат работы приложения: содержимое DOM, URL после навигации, наличие тостов-уведомлений и записи в localStorage.


<img width="974" height="1267" alt="image" src="https://github.com/user-attachments/assets/a6933ed7-465b-413c-a6e9-4d4b5ef3a8a7" />

Рис.1. Результат прогона E2E-тестов (18 passed, 11.2 s)

## 1.2. Применение Page Object Model
В работе использован паттерн Page Object Model (POM). Его основная идея — разделение логики взаимодействия со страницами и самих тестовых сценариев. Тест описывает что проверяется, а Page Object инкапсулирует как добраться до нужного элемента.
Дополнительно введён базовый класс BasePage, который содержит общие методы (открытие страницы, ожидание тостов) и наследуется остальными объектами страниц.

```
e2e/
├─ fixtures/
│  └─ pages.ts            # фикстуры, внедряющие Page Objects в тест
├─ pages/
│  ├─ BasePage.ts         # базовый класс: open(), waitForToast()
│  ├─ SignupPage.ts       # регистрация нового пользователя
│  ├─ LoginPage.ts        # авторизация
│  ├─ Navbar.ts           # навигация, проверка статуса логина, logout
│  ├─ ProductsPage.ts     # каталог, поиск, карточка товара
│  ├─ CartPage.ts         # корзина, удаление товара
│  ├─ CheckoutPage.ts     # форма оформления заказа
│  └─ PlacedOrderPage.ts  # подтверждение заказа
├─ support/
│  ├─ UserFactory.ts      # фабрика тестовых пользователей
│  └─ helpers.ts          # registerAndLogin(page)
├─ tests/
│  ├─ 01-registration.spec.ts
│  ├─ 02-login-logout.spec.ts
│  ├─ 03-product-search.spec.ts
│  ├─ 04-cart.spec.ts
│  └─ 05-checkout.spec.ts
└─ playwright.config.ts
```

Рис.2. Структура тестового проекта e2e/.

## Назначение классов:
1. `BasePage.ts` — открытие страницы по относительному URL и ожидание тостов с заданным текстом или регулярным выражением.
2. `SignupPage.ts` — регистрация нового пользователя через placeholder-локаторы Name/Email/Password и кнопку Sign Up.
3. `LoginPage.ts` — авторизация через input[type=email] / input[type=password] и кнопку Login.
4. `Navbar.ts` — навигационные ссылки, проверка статуса logged-in/logged-out, logout.
5. `ProductsPage.ts` — каталог товаров, поиск по названию, переход в карточку, добавление в корзину.
6. `CartPage.ts` — отображение товаров в корзине, удаление позиции, переход к оформлению.
7. `CheckoutPage.ts` — заполнение формы доставки и подтверждение заказа.
8. `PlacedOrderPage.ts` — проверка факта успешного оформления заказа.
Используемые data-testid: product-card, product-card-title, product-price, add-to-cart, search-input, cart-item, cart-empty, cart-remove, cart-checkout, checkout-total, order-placed, product-details, size-{размер}. Регистрация опирается на placeholder Name/Email/Password и кнопку Sign Up; вход — на input[type=email] / input[type=password] и кнопку Login.

## 1.3. Исходный код Page Object
•	[pages/BasePage.ts](https://github.com/ShpakN/testback/blob/main/e2e/pages/BasePage.ts)

•	[pages/SignupPage.ts](https://github.com/ShpakN/testback/blob/main/e2e/pages/SignupPage.ts)

•	[pages/LoginPage.ts](https://github.com/ShpakN/testback/blob/main/e2e/pages/LoginPage.ts)

•	[pages/Navbar.ts](https://github.com/ShpakN/testback/blob/main/e2e/pages/Navbar.ts)

•	[pages/ProductsPage.ts](https://github.com/ShpakN/testback/blob/main/e2e/pages/ProductsPage.ts)

•	[pages/CartPage.ts](https://github.com/ShpakN/testback/blob/main/e2e/pages/CartPage.ts)

•	[pages/CheckoutPage.ts](https://github.com/ShpakN/testback/blob/main/e2e/pages/CheckoutPage.ts)

•	[pages/PlacedOrderPage.ts](https://github.com/ShpakN/testback/blob/main/e2e/pages/PlacedOrderPage.ts)

## 1.4. Фикстуры и внедрение Page Objects
•	[fixtures/pages.ts](https://github.com/ShpakN/testback/blob/main/e2e/fixtures/pages.ts)

## 1.5. Исходный код Е2Е-тестов:
•	[01-registration.spec.ts](https://github.com/ShpakN/testback/blob/main/e2e/tests/01-registration.spec.ts) — регистрация пользователя

•	[02-login-logout.spec.ts](https://github.com/ShpakN/testback/blob/main/e2e/tests/02-login-logout.spec.ts) — вход и выход

•	[03-product-search.spec.ts](https://github.com/ShpakN/testback/blob/main/e2e/tests/03-product-search.spec.ts) — поиск товара

•	[04-cart.spec.ts](https://github.com/ShpakN/testback/blob/main/e2e/tests/04-cart.spec.ts) — добавление товара в корзину и удаление

•	[05-checkout.spec.ts](https://github.com/ShpakN/testback/blob/main/e2e/tests/05-checkout.spec.ts) — оформление заказа

## 1.6. Конфигурация Playwright
•	[playwright.config.ts](https://github.com/ShpakN/testback/blob/main/e2e/playwright.config.ts)

## Часть 2. Пирамида тестирования
## 2.1. Схема пирамиды
Пирамида тестирования для интернет-магазина Edgistify построена по трём уровням: unit (модульные), integration (интеграционные) и E2E (сквозные). Широкое основание — быстрые и дешёвые проверки изолированных функций (Unit (дешёвые, их больше)); узкая вершина — дорогие, но наиболее близкие к реальности сквозные сценарии (E2E (самые дорогие, но их меньше)).
<img width="734" height="463" alt="Снимок экрана (2706)" src="https://github.com/user-attachments/assets/190a0fcb-f766-4592-bdf8-1e2f56fa8d53" />

Рис.3. Пирамида тестирования проекта Edgistify: 46 автотестов на трёх уровнях (Unit 15, Integration 13, E2E 18).
## 2.2. Распределение тестов
| Уровень | Количество | Доля | Инструмент | Время | Результат |
|---|:--:|:--:|---|---|:--:|
| Unit | 15 | 33 % | Vitest 4.1.12 + @vitest/coverage-v8 | 0,9 с | PASSED |
| Integration | 13 | 28 % | Node Test Runner + supertest + mongodb-memory-server | 1,1 с | PASSED |
| E2E | 18 | 39 % | Playwright + Chromium | 11,2 с | PASSED |
| **Всего** | **46** | **100 %** | — | **13,2 с** | **PASSED** |

## 2.3. Unit-тестирование
Модульные тесты реализованы с помощью `Vitest v4.1.12`. Запуск — `npm run test:unit`.

Объект тестирования — модуль `frontend/src/utils/cart.ts`, вынесенный из компонентов `Product.tsx`, `ProductDetails.tsx` и `Cart.tsx`. 

Проверяемые функции

`calculateTotal(items)` — суммирование стоимости корзины:

1.	Суммирование цены с количеством.
2.	Пустая корзина возвращает 0.
`buildCartPayload(product)` — сборка тела запроса для `POST /api/cart/add`:
3.	Поле images всегда отдаётся массивом.
4.	price приводится к числу.

Результат: 4/4 PASSED.

## Unit-тесты (15) — Vitest
•	[frontend/vitest.config.ts](https://github.com/ShpakN/testback/blob/main/frontend/vitest.config.ts)

•	[frontend/src/utils/cart.test.ts](https://github.com/ShpakN/testback/blob/main/frontend/src/utils/cart.test.ts)

•	[frontend/src/utils/cart.ts](https://github.com/ShpakN/testback/blob/main/frontend/src/utils/cart.ts)

Кроме того, тесты закрепляют контракт функции: изменение сигнатуры `buildCartPayload` или удаление нормализации `images` сразу уронит прогон.
## Результат прогона

<img width="974" height="1117" alt="image" src="https://github.com/user-attachments/assets/9e8e86f6-fa6f-4aeb-b371-715ec65b2858" />

Рис.2. Результат прогона unit-тестов (4 passed, 852 ms)

Сами тесты занимают 5 миллисекунд — меньше одной сотой от общего времени. Остальное уходит на подъём окружения jsdom и трансформацию модулей. Это показывает главный принцип пирамиды: модульные проверки практически бесплатны, поэтому их должно быть много. Для сравнения, один `E2E-тест` в `Playwright` выполняется от 0,8 до 10 секунд — в тысячи раз дольше.

Покрытие 100 % относится к модулю `cart.ts`, включённому в конфигурацию `Vitest` через c `overage.include`, а не ко всему приложению. Без ограничения `include Vitest` посчитал бы весь `frontend`, и общий процент составил бы около 15 %.
## 2.4. Интеграционное тестирование
Для интеграционного тестирования использован встроенный `Node.js Test Runner (node --test)`. Тесты проверяют взаимодействие `REST API` с базой данных `MongoDB`.
В качестве базы данных применяется `MongoDB in-memory (mongodb-memory-server)`: экземпляр поднимается перед прогоном и гасится после, поэтому тесты изолированы от рабочей базы и не требуют внешнего сервера. HTTP-запросы отправляются через `Supertest` напрямую в Express-приложение, без запуска `listen` на порту.
Реализованные проверки

Каталог товаров (`GET /api/products`)
1.	Каталог отвечает статусом 200 и возвращает массив товаров.
2.	Созданный товар сохраняется в БД и возвращается со всеми полями `title` и `price`.
3.	Схема `ProductModel` содержит `title` и `price` как обязательные поля.
4.	Документ без `title` не сохраняется — срабатывает валидация `Mongoose`.
5.	Получение одного товара по идентификатору (`GET /api/products/:id`).
Корзина (`POST /api/cart/add`)
6.	Запрос без поля `images` отклоняется со статусом 400.
7.	Запрос, где `images` передан строкой вместо массива, отклоняется со статусом 400.
8.	Запрос без `JWT` возвращает 401.
9.	Корректный `payload` с массивом `images` создаёт позицию корзины со статусом 201.
Заказы (`POST /api/orders/create`)
10.	Запрос без `JWT` возвращает 401.
11.	Запрос с невалидным `JWT` возвращает 401.
12.	Заказ сохраняется с реальным `userId`, взятым из токена.
13.	Поле `userId` в теле запроса игнорируется — защита от подмены авторства заказа.
Тесты отправляют реальные HTTP-запросы к приложению, проверяют коды ответов и тело ответа, а также состояние базы данных после операции. 

## Результат: 13/13 PASSED.

<img width="974" height="1457" alt="image" src="https://github.com/user-attachments/assets/f519eef1-8315-44e6-8d3d-612ac0562d75" />

<img width="974" height="879" alt="image" src="https://github.com/user-attachments/assets/35968172-c86e-40f3-9d8f-c7875548ea2b" />

Рис.3. Интеграционные тесты API: 13/13 PASSED после исправления тестовых данных (сверху — диагностический прогон с 1 падением).

## 2.5. E2E-тестирование
E2E-тестирование реализовано через `Playwright` (`проект chromium`). Тесты проверяют приложение со стороны пользователя: открытие страниц, ввод данных, нажатие кнопок, работу корзины и оформление заказа.

| Файл | Тестов | Статус | Время |
|---|:--:|:--:|:--:|
| `01-registration.spec.ts` | 3 | PASSED | — |
| `02-login-logout.spec.ts` | 5 | PASSED | — |
| `03-product-search.spec.ts` | 4 | PASSED | — |
| `04-cart.spec.ts` | 3 | PASSED | 4,9 с |
| `05-checkout.spec.ts` | 2 | PASSED | 4,75 с |
| **Всего** | **18** | **PASSED** | **11,2 с** |

## 2.6. Обоснование пирамиды 
Пирамида тестирования в проекте выстроена снизу вверх: 15 unit-тестов Vitest проверяют чистую логику `frontend/src/utils/cart.ts` за доли секунды (покрытие 100 % при пороге 80 %), 13 интеграционных тестов на Node Test Runner и Supertest с MongoDB in-memory проверяют контракты REST API — каталог, корзину и оформление заказа, — 18 E2E-сценариев Playwright в Chromium покрывают путь пользователя целиком за ~11 с.

Превышение числа E2E над unit объясняется характером приложения: основная логика живёт в React-компонентах и обработчиках Express, где изоляция теряет диагностическую ценность. Соотношение 15 : 13 : 18 сохраняет главный принцип пирамиды — быстрые уровни (28 тестов, 61 %) дают точную локализацию ошибок за секунды, дорогие E2E (18 тестов, 39 %) подтверждают работу приложения для пользователя. Совместный прогон всех 46 тестов занимает около 13 с и даёт 46/46 PASSED.

## Часть 3. CI/CD и Quality Gates

## 3.1. Для автоматического запуска проверок в проекте настроен GitHub Actions — облачный CI-сервис, встроенный в GitHub.

Файл конфигурации: [.github/workflows/ci.yml](https://github.com/ShpakN/testback/blob/main/.github/workflows/ci.yml)

Репозиторий: [github.com/ShpakN/testback](https://github.com/ShpakN/testback/tree/main)

## 3.2. Структура CI/CD-пайплайна

<img width="506" height="719" alt="Снимок экрана (2707)" src="https://github.com/user-attachments/assets/7415960a-18b2-450f-8e61-fc68af6bf73a" />

## 3.3. Этапы пайплайна

| Этап | Job | Выполняемые действия |
|---|---|---|
| Unit, Lint and Coverage | `unit` | `npm ci`, `npm run lint` (ESLint), `npm run test:coverage` — 15 unit-тестов с порогом 80 %, выгрузка coverage-отчёта |
| Security Audit | `security` | `npm ci` в `frontend` и `backend`, `npm audit --audit-level=critical` в обеих папках, сканирование секретов Gitleaks |
| Integration Tests | `integration` | `npm ci` в `backend`, ожидание готовности MongoDB, `npm run test:integration` |
| Playwright E2E | `e2e` | `npm ci` во всех трёх пакетах, ожидание MongoDB, seed базы, проверка что товары появились, установка Chromium, `npx playwright test --project=chromium` |
| Build | `build` | `npm ci`, `npm run build` во `frontend`, публикация `dist/` как артефакта |

Перед `E2E` дополнительно выполняется наполнение базы тестовыми товарами (`npm run seed`) и проверка, что в коллекции products ненулевое число документов — иначе пайплайн падает с понятным сообщением `products in DB: 0`, а не с 54 таймаутами `Playwright`.

## 3.4. Блокирующие Quality Gates

| Название | Условие блокировки |
|---|---|
| Unit Quality Gate | Если хотя бы один модульный тест завершается с ошибкой, `unit` получает статус Failed. Job'ы `integration`, `e2e` и `build` объявлены с `needs`, содержащим `unit`, поэтому не стартуют и получают статус Skipped. |
| Coverage Quality Gate | Минимально допустимое покрытие задано в `vitest.config.ts` — 80 % по всем четырём метрикам (`statements`, `branches`, `functions`, `lines`). При недостаточном покрытии Vitest возвращает ненулевой код, и `unit` падает. |
| Security Quality Gate | `npm audit --audit-level=critical` выполняется отдельно для `frontend` и `backend`. Critical-уязвимость → ненулевой exit code → `security` Failed → `build` Skipped. |
| Gitleaks Gate | Сканирование истории на секреты; обнаружение ключа → `security` Failed → `build` Skipped. |
| E2E Gate | Падение любого из 18 E2E-тестов → `e2e` Failed → `build` Skipped. |
| Integration Gate | Падение любого из 13 интеграционных тестов → `integration` Failed → `build` Skipped. |
| Build Gate | `build` объявлен как `needs: [unit, security, integration, e2e]` — production-сборка запускается только после успеха всех четырёх предыдущих. При ошибке любой обязательной проверки сборка остаётся в статусе Skipped. |
| Branch Protection | Правило защиты ветки настраивается в Settings → Branches → Add branch protection rule и требует административных прав на репозиторий. |

## 3.5 Практическая проверка Quality Gates
Для подтверждения работы блокирующих проверок проведены отдельные эксперименты: намеренно вносились ошибки, и проверялось, что пайплайн останавливается на нужной стадии.
## 3.5.1. Проверка Unit Quality Gate
В набор unit-тестов временно добавлен тест с заведомо ошибочным утверждением (`expect(1).toBe(2)`).

Результат прогона (из общего набора 15 unit-тестов упал один):

| Job | Статус |
|---|---|
| Unit, Lint and Coverage | **Failed** (14 passed, 1 failed) |
| Security Audit | Skipped |
| Integration Tests | Skipped |
| Playwright E2E | Skipped |
| Build | Skipped |

Ошибка unit-теста заблокировала все последующие стадии.

<img width="1006" height="502" alt="image" src="https://github.com/user-attachments/assets/db5dddfb-a907-4a64-9aa7-71fbff1a6202" />

Рис.4.  Блокировка пайплайна при падении unit-тестов. 
## 3.5.2. Проверка Coverage Quality Gate
Для проверки порога в тестируемый модуль `src/utils/cart.ts` добавлен код, который не вызывается ни одним тестом. Все 15 unit-тестов остались зелёными (`Tests 15 passed (15)`), но покрытие упало ниже установленного порога.

| Метрика | Фактическое покрытие | Требование |
|---|:--:|:--:|
| Statements | 53,33 % | 80 % |
| Branches | 68,42 % | 80 % |
| Functions | 80,00 % | 80 % |
| Lines | 54,54 % | 80 % |

Vitest вывел три ошибки и завершился с кодом 1:

ERROR: Coverage for lines (54.54%) does not meet global threshold (80%)

ERROR: Coverage for statements (53.33%) does not meet global threshold (80%)

ERROR: Coverage for branches (68.42%) does not meet global threshold (80%)

$ echo "Exit code: $LASTEXITCODE"

Exit code: 1

Ненулевой код возврата валит job unit, а вслед за ним не запускаются security, integration, e2e и build — они получают статус Skipped. Так подтверждена работа Coverage Quality Gate.

<img width="974" height="1271" alt="image" src="https://github.com/user-attachments/assets/3a671d7e-73d6-42ed-b8bc-1b56451536c9" />

Рис.5. Проверка Coverage Quality Gate. 
## 3.5.3. Проверка Security Quality Gate
Результат прогона:

| Job | Статус |
|---|---|
| Unit, Lint and Coverage | **Success** |
| Security Audit | **Failed** |
| Integration Tests | Skipped |
| Playwright E2E | Skipped |
| Build | Skipped |

В frontend установлен `form-data@2.0.0` с critical-уязвимостью

<img width="974" height="1015" alt="image" src="https://github.com/user-attachments/assets/642d06e5-99d5-44d3-ab95-b6e80f2272ea" />

Рис.6. Проверка Security Quality Gate
## 3.5.4. Успешный запуск CI/CD
После устранения ошибок пайплайн успешно выполнил все пять заданий.

| Job | Время | Статус |
|---|:--:|---|
| Unit, Lint and Coverage | 17 с | Success |
| Security Audit | 53 с | Success |
| Integration Tests | 18 с | Success |
| Playwright E2E | 1 м 56 с | Success |
| Build (production) | 14 с | Success |
| **Всего** | **2 м 19 с** | **5/5 SUCCESS** |

<img width="996" height="502" alt="image" src="https://github.com/user-attachments/assets/604d51ce-af8e-4829-857f-daa88a6e191d" />

Рис.7. Успешное прохождение всех пяти заданий пайплайна

## 3.6. Локальный запуск тестов
Для локального воспроизведения проверок используется `Node.js 22`. Перед интеграционными и E2E-тестами необходимо запустить `MongoDB`, `backend` и `frontend`, а также подготовить тестовые данные.
## 3.6.1. Модульные тесты
Из папки `frontend`:
```bash
npm ci
npm run test:unit
```
Результат локального прогона: `Tests 15 passed (15)`, длительность около 0,85 с.
## 3.6.2. Проверка покрытия
`npm run test:unit:coverage`
Порог 80% настроен в `vitest.config.ts` — при недостаточном покрытии команда завершится с ненулевым кодом.
3.6.3. Статический анализ и сборка
```bash
npm run lint
npm run build
```
## 3.6.4. Интеграционные тесты
Из папки `backend` при работающих `MongoDB` и `backend`:
```bash
npm ci
npm run test:integration
```
В `CI` эта команда даёт `# tests 13`, `# pass 13`. Локально без поднятой `MongoDB` тесты упадут на подключении в `config/db.js` с ошибкой `«в .env не задан MONGO_URI»` или отказом соединения, поэтому перед запуском надо создать `.env` в `backend` с `MONGO_URI` и `JWT_SECRET`.
## 3.6.5. E2E-тесты
Из папки `e2e` при запущенном приложении:
```bash
npm ci
npx playwright install chromium
npx playwright test --project=chromium
```
Кроме того, `Playwright` настраивает `webServer` и сам поднимает `backend` и `frontend` (когда `BASE_URL` не задан внешний). В `CI` прогоняется только проект `chromium` — 18 тестов, около 11,2 с.
## 3.6.6. Проверка зависимостей
Из папок `frontend` и `backend` отдельно:
```bash
npm audit --audit-level=critical
```
В `CI` подготовка окружения и запуск проверок выполняются автоматически.

## 3.7. Итоговые результаты
| Проверка | Результат |
|---|---|
| Unit-тестирование | 15/15 PASSED |
| Integration-тестирование | 13/13 PASSED |
| E2E-тестирование (Chromium) | 18/18 PASSED |
| **Общее количество тестов** | **46** |
| Покрытие `src/utils/cart.ts` | 100 % |
| Порог Coverage Gate | 80 % |
| ESLint | PASSED |
| Production Build | PASSED |
| Security Audit | PASSED (0 critical) |
| Gitleaks | PASSED (no leaks detected) |
| Unit Quality Gate | Проверен (падает при ошибке теста) |
| Coverage Quality Gate | Проверен (падает при покрытии < 80 %) |
| Security Quality Gate | Проверен (падает при critical-уязвимостях) |
| GitHub Actions | 5/5 SUCCESS |

## 3.8. Использованные коммиты
| Коммит | Описание |
|---|---|
| [`854c2d6`](https://github.com/ShpakN/testback/commit/854c2d6) | ci: switch to npm ci, add PR trigger, gate build on e2e |
| [`1932396`](https://github.com/ShpakN/testback/commit/1932396) | fix(deps): remove unused native bcrypt; drops vulnerable tar |
| [`2cf6e5d`](https://github.com/ShpakN/testback/commit/2cf6e5d) | ci: restore MONGO_URI + mongo service for integration, seed db before e2e; fix vite proxy to 127.0.0.1 |
| [`1b9ed4d`](https://github.com/ShpakN/testback/commit/1b9ed4d) | chore: add .gitattributes for consistent LF endings |
| [`b165bc8`](https://github.com/ShpakN/testback/commit/b165bc8) | chore: add CI status badge to README |

## 4. Ответы на контрольные вопросы
## 1. Что такое пирамида тестирования и почему она важна?
Пирамида тестирования — модель распределения автотестов по уровням: много быстрых и дешёвых тестов внизу, мало медленных и дорогих наверху.

Важность для CI: пирамида определяет, где ставить quality gate. Быстрые unit гоняются на каждый коммит, E2E — только после них, иначе разработчик ждёт 5 минут из-за одной опечатки.
## 2. Какие паттерны автоматизации UI вы знаете?

**Page Object Model (POM)** — каждая страница описывается отдельным классом, тест работает с методами, а не с локаторами. Локаторы собраны в одном месте (изменился `data-testid` — правится один файл), тест читается как сценарий, объекты переиспользуются. В проекте: `e2e/pages/ProductsPage.ts`, `e2e/pages/BasePage.ts`.

**Service Object / API-хелперы** — работа с HTTP вынесена в отдельный слой (`api.signup(user)`). Данные для UI-теста готовятся через API, минуя интерфейс: быстрее и надёжнее. Классический приём — логин через API, проверка через UI. В проекте: `e2e/support/helpers.ts` (`registerAndLogin`).

**Factory / Builder** — `makeUser({ email: uniqueEmail() })` вместо ручного конструирования. Решает проблему дубликатов email в параллельных прогонах. В проекте: `e2e/support/UserFactory.ts`.

**Fixtures** — внедрение зависимостей в Playwright: тест получает готовые Page Objects параметром, без `new` в каждом тесте. В проекте: `e2e/fixtures/pages.ts`.

## 3. Что такое quality gates и зачем они нужны?

Quality gate — обязательное условие в CI/CD, без выполнения которого пайплайн останавливается и артефакт не идёт дальше (в `main`, на staging, в релиз). Это не рекомендация, а блокирующий автоматический фильтр.

Зачем нужны:
- **Предсказуемость `main`** — в основную ветку не попадает код с упавшими тестами.
- **Быстрая обратная связь** — о поломке узнаётся через 2 минуты, а не на ревью или в проде.
- **Снятие человеческого фактора** — не зависит от того, вспомнит ли проверяющий запустить тесты.
- **Защита от деградации** — порог покрытия и audit не дают коду тихо портиться мелкими коммитами.
- **Ускорение ревью** — ревьюер смотрит логику, а не «прошли ли тесты».

Реализация в проекте через `needs` в GitHub Actions:

| Gate | Критерий | Что блокируется |
|---|---|---|
| Unit | все 15 тестов зелёные | `integration`, `e2e`, `build` |
| Coverage | ≥ 80 % по statements / branches / functions / lines | job `unit` падает |
| Security | `npm audit --audit-level=critical` = 0 уязвимостей | job `build` |
| Integration | 13 API-тестов против MongoDB | job `build` |
| E2E | 18 тестов проходят в Chromium | job `build` |
| Branch protection | все проверки зелёные | merge в `main` запрещён |

## 4. Почему unit на каждый коммит, integration — после сборки, E2E — перед релизом?

Принцип один: чем дороже проверка, тем реже её запускают.

**Unit — на каждый коммит (push и PR).** Весь набор выполняется за ~0,85 с. Цель — мгновенная обратная связь, пока разработчик не переключился на другую задачу. Работает принцип «сломанного окна»: если CI красный больше часа, на него перестают смотреть. При тысячах тестов переходят на прогон только затронутых (`vitest --changed`).

**Integration — после сборки.** Нужна инфраструктура (MongoDB, backend), локально её держат не всегда. Запуск после сборки логичен: если код не компилируется, интеграционные тесты упадут по той же причине, но с ложным диагнозом. Проверяют контракт API, работу с БД и авторизацию — то, чего unit-тесты с моками не видят. В CI — 18 с на 13 тестов.

**E2E — перед сдачей, после всех зелёных стадий.** Полный набор в Chromium — 1 м 56 с на 18 тестов; матрица Chromium + Firefox + WebKit + мобильные — часы. Уровень хрупкий: таймауты, сеть, seed базы, состояние данных. Плохое соотношение «цена / сигнал» (минуты ожидания ради проверки одной строки) и риск флаков, после которых CI перестают доверять. Зато ловит то, что не видит никто другой: интеграцию фронта и бэка в браузере, роутинг, сохранение токена, поведение после reload.
## 5. Вывод
Выполнение лабораторной работы показало, что автоматизация — не «проверочная надстройка» над готовым кодом, а конструкция самого процесса разработки. CI/CD перестаёт быть набором ручных действий «прогнать тесты перед пушем» и становится воспроизводимым контрактом: любое изменение проходит один и тот же путь проверок.

Главный результат: в ветку `main` не может попасть код, не прошедший тесты. Это обеспечивают блокирующие quality gates и branch protection. Пайплайн выстроен по пирамиде тестирования — 15 unit-тестов (0,85 с), 13 интеграционных против реальной MongoDB, 18 E2E в Chromium — и запускает проверки по возрастанию стоимости, давая обратную связь за секунды вместо минут.

**Негативные эксперименты** подтвердили, что каждый gate действительно блокирует пайплайн:

| Эксперимент | Результат |
|---|---|
| Ложное утверждение в unit-тесте | `unit` — Failed, `integration` / `e2e` / `build` — Skipped |
| Код без тестов в `cart.ts` | 15 тестов зелёные, покрытие 53,33 % / 68,42 % / 54,54 % → Exit code: 1 |
| `form-data@2.0.0` с critical-уязвимостью | `security` — Failed, `build` — Skipped |

**Реальные сбои CI, не воспроизводившиеся локально**, были найдены автоматически: нативный `bcrypt`, тянувший уязвимый `tar` (в коде используется `bcryptjs`); рассинхронизация `package-lock.json` и `package.json`, ломавшая `npm ci`; Vite-прокси на `localhost:5000`, из-за которого на Ubuntu запросы уходили в IPv6 и висели до таймаута Playwright; пустая база из-за невыполненного `seed` перед E2E; несуществующий ключ `navigationWaitUntil` в конфиге Playwright.

Итоговая конфигурация `.github/workflows/ci.yml` обеспечивает полный цикл — линтинг, unit-тесты с порогом покрытия 80 %, аудит зависимостей, Gitleaks, интеграционное и E2E-тестирование, production-сборку — за **2 минуты 19 секунд** без участия человека.
